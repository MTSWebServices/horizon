# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from horizon.backend.providers.auth import AuthProvider
from horizon.backend.services.auth import get_auth_provider
from horizon.backend.services.uow import UnitOfWork
from horizon.commons.errors import get_error_responses
from horizon.commons.errors.schemas import InvalidRequestSchema, NotAuthorizedSchema
from horizon.commons.schemas.v1 import AuthTokenResponseV1

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/token",
    summary="Get access token",
    responses=get_error_responses(include={NotAuthorizedSchema, InvalidRequestSchema}),
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
    uow: Annotated[UnitOfWork, Depends()],
) -> AuthTokenResponseV1:
    token = await auth_provider.get_token(
        uow=uow,
        grant_type=form_data.grant_type,
        login=form_data.username,
        password=form_data.password,
        scopes=form_data.scopes,
        client_id=form_data.client_id,
        client_secret=form_data.client_secret,
    )
    return AuthTokenResponseV1.model_validate(token)
