from fastapi import Request

from horizon.backend.providers.auth.base import AuthProvider


async def get_auth_provider(request: Request) -> AuthProvider:
    return request.app.state.auth_provider
