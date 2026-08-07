# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

"""
AuthProvider using LDAP for checking user existence and credentials.

Based on `bonsai <https://github.com/noirello/bonsai>`_

Similar to:
* `JupyterHub LDAPAuthenticator <https://github.com/jupyterhub/ldapauthenticator>`_
* `Flask-AppBuilder LDAP integration <https://github.com/dpgaspar/Flask-AppBuilder/blob/master/docs/config.rst>`_,
used in Apache Airflow
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from time import time
from typing import Any

from bonsai import InvalidDN, LDAPClient
from bonsai.asyncio import AIOConnectionPool, AIOLDAPConnection
from bonsai.errors import AuthenticationError, LDAPError
from devtools import pformat
from fastapi import FastAPI

from horizon.backend.db.models import User
from horizon.backend.providers.auth.base import AuthProvider
from horizon.backend.services.uow import UnitOfWork
from horizon.backend.settings.auth.ldap import LDAPAuthProviderSettings
from horizon.backend.utils.jwt import decode_jwt, sign_jwt
from horizon.commons.exceptions import (
    AuthorizationError,
    EntityNotFoundError,
    ServiceError,
)

log = logging.getLogger(__name__)

LDAPUnrecoverableError = (LDAPError, TimeoutError)


class LDAPAuthProvider(AuthProvider):
    def __init__(
        self,
        auth_settings: LDAPAuthProviderSettings,
        pool: AIOConnectionPool | None,
    ) -> None:
        self._pool: AIOConnectionPool | None = pool
        self._auth_settings: LDAPAuthProviderSettings = auth_settings

    @classmethod
    def setup(cls, app: FastAPI) -> FastAPI:
        auth_settings = LDAPAuthProviderSettings.model_validate(app.state.settings.auth.dict(exclude={"provider"}))
        log.info("Using %s provider with settings:\n%s", cls.__name__, pformat(auth_settings))
        pool = cls._create_lookup_pool(auth_settings)
        app.state.auth_provider = cls(auth_settings=auth_settings, pool=pool)
        return app

    async def get_current_user(self, access_token: str, uow: UnitOfWork) -> User:
        if not access_token:
            msg = "Missing auth credentials"
            raise AuthorizationError(msg)

        user_id = self._get_user_id_from_token(access_token)
        user = await uow.user.get_by_id(user_id)
        if not user.is_active:
            msg = f"User {user.username!r} is disabled"
            raise AuthorizationError(msg)
        return user

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

        # firstly check if user exists in LDAP and credentials are valid
        username = await self._resolve_username_from_ldap(login, password)

        log.info("Get/create user %r in database", username)
        async with uow:
            # and only then create user in database.
            # avoid creating fake users by spamming auth endpoint
            user = await uow.user.get_or_create(username=username)

        log.info("User id %r found", user.id)
        if not user.is_active:
            # TODO: check if user is locked in LDAP
            msg = f"User {username!r} is disabled"
            raise AuthorizationError(msg)

        log.info("Generate access token for user id %r", user.id)
        access_token, expires_at = self._generate_access_token(user)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_at": expires_at,
        }

    @classmethod
    def _get_lookup_client(cls, settings: LDAPAuthProviderSettings) -> LDAPClient:
        """Create client for lookup queries"""
        client = LDAPClient(str(settings.ldap.url))
        if settings.ldap.lookup.credentials:
            client.set_credentials(
                settings.ldap.auth_mechanism,
                settings.ldap.lookup.credentials.user,
                settings.ldap.lookup.credentials.password.get_secret_value(),
            )
        return client

    @classmethod
    def _create_lookup_pool(cls, settings: LDAPAuthProviderSettings) -> AIOConnectionPool | None:
        """Create and check connection pool for lookup queries"""
        if not settings.ldap.lookup.enabled:
            return None

        client = cls._get_lookup_client(settings)
        if settings.ldap.lookup.check_on_startup:
            try:
                client.connect(timeout=settings.ldap.timeout_seconds)
            except LDAPError as e:
                msg = "Failed to connect to LDAP"
                raise ServiceError(msg) from e

        if not settings.ldap.lookup.pool.enabled:
            return None

        log.debug("Lookup enabled, creating connection pool")
        return AIOConnectionPool(
            client,
            minconn=settings.ldap.lookup.pool.initial,
            maxconn=settings.ldap.lookup.pool.max,
            timeout=settings.ldap.timeout_seconds,
        )

    @asynccontextmanager
    async def _get_lookup_connection(self) -> AsyncGenerator[AIOLDAPConnection, None]:
        """Create connection used for lookup queries"""
        try:
            connect: AbstractAsyncContextManager[AIOLDAPConnection]
            if self._pool:
                log.debug("Using lookup pool")
                connect = self._pool.spawn()

            else:
                log.debug("Creating non-pooled connection for lookup")
                client = self._get_lookup_client(self._auth_settings)
                connect = client.connect(is_async=True, timeout=self._auth_settings.ldap.timeout_seconds)

            async with connect as connection:
                try:
                    yield connection
                except LDAPUnrecoverableError:
                    # avoid returning connection back to the pool
                    # https://bonsai.readthedocs.io/en/latest/advanced.html#connection-timeouts
                    connection.close()
                    raise

        except LDAPUnrecoverableError as e:
            msg = "Failed to connect to LDAP"
            raise ServiceError(msg) from e

    async def _resolve_username_from_ldap(self, login: str, password: str) -> str:
        log.info("Resolve user %r in LDAP", login)
        username = login

        if self._auth_settings.ldap.lookup.enabled:
            log.info("Perform lookup in LDAP")
            dn, username = await self._lookup_user(login)
        else:
            dn = self._auth_settings.ldap.bind_dn_template.format(
                login=login,
                base_dn=self._auth_settings.ldap.base_dn,
                uid_attribute=self._auth_settings.ldap.uid_attribute,
            )

        log.info("Check user credentials %r in LDAP", dn)
        await self._login(dn, password)

        return username

    async def _lookup_user(self, login: str) -> tuple[str, str]:
        # Reference implementations:
        # https://github.com/dpgaspar/Flask-AppBuilder/blob/2c5763371b81cd679d88b9971ba5d1fc4d71d54b/flask_appbuilder/security/manager.py#L902
        # https://github.com/jupyterhub/ldapauthenticator/blob/main/ldapauthenticator/ldapauthenticator.py
        query = self._auth_settings.ldap.lookup.query_template.format(
            login=login,
            uid_attribute=self._auth_settings.ldap.uid_attribute,
        )
        base_dn = self._auth_settings.ldap.base_dn
        scope = self._auth_settings.ldap.lookup.scope
        log.debug("Lookup query: %r", query)
        log.debug("Base DN: %r", base_dn)
        log.debug("Scope: %r", scope)

        async with self._get_lookup_connection() as connection:
            results = await connection.search(
                base=base_dn,
                scope=scope,
                filter_exp=query,
                attrlist=["*"],
                sizelimit=1,
                timeout=self._auth_settings.ldap.timeout_seconds,
            )

        if not results:
            raise EntityNotFoundError("User", "username", login)

        entry = results[0]
        log.debug("Found entry:\n%s", pformat(entry))
        dn = str(entry["dn"])
        uid = entry[self._auth_settings.ldap.uid_attribute][0]
        return dn, uid

    async def _login(self, login: str, password: str):
        client = LDAPClient(str(self._auth_settings.ldap.url))
        client.set_credentials(self._auth_settings.ldap.auth_mechanism, login, password)
        try:
            connection = client.connect(is_async=True, timeout=self._auth_settings.ldap.timeout_seconds)
            async with connection:
                await connection.whoami()
        except (AuthenticationError, InvalidDN) as e:
            msg = "Wrong credentials"
            raise AuthorizationError(msg) from e
        except LDAPUnrecoverableError as e:
            msg = "Failed to connect to LDAP"
            raise ServiceError(msg) from e

    def _generate_access_token(self, user: User) -> tuple[str, float]:
        expires_at = time() + self._auth_settings.access_token.expire_seconds
        payload = {
            "user_id": user.id,
            "exp": expires_at,
        }
        access_token = sign_jwt(
            payload,
            self._auth_settings.access_token.secret_key.get_secret_value(),
            self._auth_settings.access_token.security_algorithm,
        )
        return access_token, expires_at

    def _get_user_id_from_token(self, token: str) -> int:
        try:
            payload = decode_jwt(
                token,
                self._auth_settings.access_token.secret_key.get_secret_value(),
                self._auth_settings.access_token.security_algorithm,
            )
            return int(payload["user_id"])
        except (KeyError, TypeError, ValueError) as e:
            msg = "Invalid token"
            raise AuthorizationError(msg) from e
