# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0
from pydantic import BaseModel, Field

from horizon.backend.settings.auth.jwt import JWTSettings


class DummyAuthProviderSettings(BaseModel):
    """Settings for DummyAuthProvider.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      provider: horizon.backend.providers.auth.dummy.DummyAuthProvider
      access_token:
        secret_key: secret
    ```
    """

    access_token: JWTSettings = Field(description="Access-token related settings")
