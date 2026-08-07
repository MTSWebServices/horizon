# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from horizon.backend.db.models import User
from horizon.backend.providers.auth import AuthProvider
from horizon.backend.services.auth import get_auth_provider
from horizon.backend.services.uow import UnitOfWork

oauth_schema = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


async def current_user(
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
    auth_schema: Annotated[str, Depends(oauth_schema)],
    uow: Annotated[UnitOfWork, Depends()],
) -> User:
    return await auth_provider.get_current_user(auth_schema, uow)
