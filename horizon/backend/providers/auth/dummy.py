# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

import logging
from time import time
from typing import Any

from devtools import pformat
from fastapi import FastAPI

from horizon.backend.db.models import User
from horizon.backend.providers.auth.base import AuthProvider
from horizon.backend.services.uow import UnitOfWork
from horizon.backend.settings.auth.dummy import DummyAuthProviderSettings
from horizon.backend.utils.jwt import decode_jwt, sign_jwt
from horizon.commons.exceptions.auth import AuthorizationError

log = logging.getLogger(__name__)


class DummyAuthProvider(AuthProvider):
    def __init__(
        self,
        settings: DummyAuthProviderSettings,
    ) -> None:
        self._settings = settings

    @classmethod
    def setup(cls, app: FastAPI) -> FastAPI:
        settings = DummyAuthProviderSettings.model_validate(
            app.state.settings.auth.model_dump(exclude={"provider"}, warnings=False),
        )
        log.info("Initializing %s provider with settings:\n%s", cls.__name__, pformat(settings))
        app.state.auth_provider = cls(settings=settings)
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

        log.info("Get/create user %r in database", login)
        async with uow:
            user = await uow.user.get_or_create(username=login)

        log.info("Used with id %r found", user.id)
        if not user.is_active:
            msg = f"User {user.username!r} is disabled"
            raise AuthorizationError(msg)

        log.info("Generate access token for user id %r", user.id)
        access_token, expires_at = self._generate_access_token(user_id=user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_at": expires_at,
        }

    def _generate_access_token(self, user_id: int) -> tuple[str, float]:
        expires_at = time() + self._settings.access_token.expire_seconds
        payload = {
            "user_id": user_id,
            "exp": expires_at,
        }
        access_token = sign_jwt(
            payload,
            self._settings.access_token.secret_key.get_secret_value(),
            self._settings.access_token.security_algorithm,
        )
        return access_token, expires_at

    def _get_user_id_from_token(self, token: str) -> int:
        try:
            payload = decode_jwt(
                token,
                self._settings.access_token.secret_key.get_secret_value(),
                self._settings.access_token.security_algorithm,
            )
            return int(payload["user_id"])
        except (KeyError, TypeError, ValueError) as e:
            msg = "Invalid token"
            raise AuthorizationError(msg) from e
