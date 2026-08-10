# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel, ConfigDict, Field, ImportString, field_validator

from horizon.backend.providers.auth.base import AuthProvider
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

    @field_validator("provider", mode="after")
    @classmethod
    def _validate_provider(cls, value: type) -> type[AuthProvider]:
        if not issubclass(value, AuthProvider):
            msg = f"Class {value} is not a subclass of {AuthProvider}"
            raise TypeError(msg)
        return value

    # prevent leaking provider secrets
    def __repr_args__(self):
        return [("provider", self.provider)]
