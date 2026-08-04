# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends, Request
from typing_extensions import Annotated

from horizon.backend.db.repositories import (
    CredentialsCacheRepository,
    HWMHistoryRepository,
    HWMRepository,
    NamespaceHistoryRepository,
    NamespaceRepository,
    UserRepository,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session


class UnitOfWork:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        self._session = session
        self.namespace = NamespaceRepository(session=session)
        self.hwm_history = HWMHistoryRepository(session=session)
        self.namespace_history = NamespaceHistoryRepository(session=session)
        self.user = UserRepository(session=session)
        self.hwm = HWMRepository(session=session)
        self.credentials_cache = CredentialsCacheRepository(session=session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
