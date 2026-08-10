# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel, ConfigDict, Field, ImportString

from horizon.backend.providers.auth.dummy import DummyAuthProvider


class AuthSettings(BaseModel):
    """Authorization-related settings.

    Here you can set auth provider class along with its options.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      provider: horizon.backend.providers.auth.dummy.DummyAuthProvider
      access_token:
        secret_key: secret
    ```
    """

    provider: ImportString = Field(  # type: ignore[assignment]
        default=DummyAuthProvider,
        description="Full name of auth provider class",
    )

    model_config = ConfigDict(extra="allow")
