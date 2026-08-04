# SPDX-FileCopyrightText: 2025-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
from fastapi import Request

from horizon.backend.providers.auth.base import AuthProvider


async def get_auth_provider(request: Request) -> AuthProvider:
    return request.app.state.auth_provider
