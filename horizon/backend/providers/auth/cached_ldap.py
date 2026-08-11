# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

"""
AuthProvider using LDAP, but
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from bonsai.asyncio import AIOConnectionPool
from devtools import pformat
from fastapi import FastAPI
from passlib.ifc import PasswordHash
from passlib.registry import get_crypt_handler

from horizon.backend.providers.auth.ldap import LDAPAuthProvider
from horizon.backend.services.uow import UnitOfWork
from horizon.backend.settings.auth.cached_ldap import CachedLDAPAuthProviderSettings
from horizon.commons.exceptions import AuthorizationError

log = logging.getLogger(__name__)


class CachedLDAPAuthProvider(LDAPAuthProvider):
    def __init__(
        self,
        auth_settings: CachedLDAPAuthProviderSettings,
        pool: AIOConnectionPool | None,
    ) -> None:
        self._pool: AIOConnectionPool | None = pool
        self._auth_settings: CachedLDAPAuthProviderSettings = auth_settings

    @classmethod
    def setup(cls, app: FastAPI) -> FastAPI:
        auth_settings = CachedLDAPAuthProviderSettings.model_validate(
            app.state.settings.auth.model_dump(exclude={"provider"}, warnings=False)
        )
        log.info("Using %s provider with settings:\n%s", cls.__name__, pformat(auth_settings))
        pool = cls._create_lookup_pool(auth_settings)
        app.state.auth_provider = cls(auth_settings=auth_settings, pool=pool)
        return app

    async def get_token(  # noqa: PLR0917
        self,
        uow: UnitOfWork,
        grant_type: str | None = None,
        login: str | None = None,
        password: str | None = None,
        scopes: list[str] | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> dict[str, Any]:
        if not login or not password:
            msg = "Missing auth credentials"
            raise AuthorizationError(msg)

        # firstly check if user credentials already exists in cache
        from_cache = True
        username = await self._resolve_username_from_credentials_cache(login, password, uow)
        if not username:
            from_cache = False
            username = await self._resolve_username_from_ldap(login, password)

        log.info("Get/create user %r in database", username)
        async with uow:
            # and only then create user in database.
            # avoid creating fake users by spamming auth endpoint
            user = await uow.user.get_or_create(username=username)

            log.info("User id %r found", user.id)
            if not from_cache:
                # updating cache without checking user in LDAP means cache item will never expire,
                # and we will never check if used is valid
                log.info("Update credentials cache for user id %r", user.id)
                await self._update_credentials_cache(user_id=user.id, login=login, password=password, uow=uow)

        log.info("Generate access token for user id %r", user.id)
        access_token, expires_at = self._generate_access_token(user)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_at": expires_at,
        }

    def _get_hasher(self) -> PasswordHash:
        hash_settings = self._auth_settings.cache.password_hash
        handler = get_crypt_handler(hash_settings.algorithm)
        return handler.using(**hash_settings.options)

    async def _resolve_username_from_credentials_cache(self, login: str, password: str, uow: UnitOfWork) -> str | None:
        log.info("Perform lookup in credentials cache")
        user_cache = await uow.credentials_cache.get_by_login(login)
        if not user_cache:
            log.info("User %r not found in cache", login)
            return None

        log.debug("Found item %r", user_cache)
        expiration_date = user_cache.updated_at + timedelta(seconds=self._auth_settings.cache.expire_seconds)
        if expiration_date < datetime.now(tz=timezone.utc):
            log.info("Cache item expired")
            return None

        hasher = self._get_hasher()
        if not hasher.verify(password, user_cache.password_hash):
            msg = "Wrong credentials"
            raise AuthorizationError(msg)

        log.info("Credentials match the cache")
        return user_cache.user.username

    async def _update_credentials_cache(self, user_id: int, login: str, password: str, uow: UnitOfWork) -> None:
        # this is not a dedicated method of repository because we need hashing settings to generate password hash,
        # and generating new hash every time is expensive
        hasher = self._get_hasher()
        user_cache = await uow.credentials_cache.get_by_login(login=login)

        data: dict[str, Any] = {}
        if not user_cache or user_cache.user_id != user_id:
            data["user_id"] = user_id
        if not user_cache or not hasher.verify(password, user_cache.password_hash):
            data["password_hash"] = hasher.hash(password)

        # even if nothing is changed in credentials cache, we do perform an update to sync `updated_at` column
        await uow.credentials_cache.create_or_update(login=login, data=data)
