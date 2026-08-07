# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0


from horizon.backend.db.models import CredentialsCache
from horizon.backend.db.repositories.base import Repository


class CredentialsCacheRepository(Repository[CredentialsCache]):
    async def get_by_login(self, login: str) -> CredentialsCache | None:
        return await self._get(CredentialsCache.login == login)

    async def create_or_update(
        self,
        login: str,
        data: dict,
    ) -> CredentialsCache:
        result = await self._update([CredentialsCache.login == login], changes=data)
        if not result:
            result = await self._create(data={"login": login, **data})

        await self._session.flush()
        return result

    async def delete(self, id_: int) -> None:
        await self._delete(id_)
        await self._session.flush()
