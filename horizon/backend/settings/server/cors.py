# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CORSSettings(BaseModel):
    """CORS Middleware Settings.

    See [CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware) documentation.

    !!! note

        You can pass here any extra option supported by `CORSMiddleware`,
        even if it is not mentioned in documentation.

    Examples
    --------

    For development environment:

    ```yaml title="config.yml"
    server:
      cors:
        enabled: true
        allow_origins: ['*']
        allow_methods: ['*']
        allow_headers: ['*']
        expose_headers: [X-Request-ID, Location, Access-Control-Allow-Credentials]
    ```
    For production environment:

    ```yaml title="config.yml"
    server:
      cors:
        enabled: true
        allow_origins: [production.example.com]
        allow_methods: [GET]
        allow_headers: [X-Request-ID, X-Request-With]
        expose_headers: [X-Request-ID]
        # custom option passed directly to middleware
        max_age: 600
    ```
    """

    enabled: bool = Field(default=True, description="Set to `True` to enable middleware")
    allow_origins: list[str] = Field(default_factory=list, description="Domains allowed for CORS")
    allow_credentials: bool = Field(
        default=False,
        description="If `True`, cookies should be supported for cross-origin request",
    )
    allow_methods: list[str] = Field(default=["GET"], description="HTTP Methods allowed for CORS")
    # https://github.com/snok/asgi-correlation-id#cors
    allow_headers: list[str] = Field(
        default=["X-Request-ID", "X-Request-With"],
        description="HTTP headers allowed for CORS",
    )
    expose_headers: list[str] = Field(default=["X-Request-ID"], description="HTTP headers exposed from backend")

    @field_validator("allow_origins", "allow_methods", "allow_headers", "expose_headers", mode="before")
    @classmethod
    def _validate_bootstrap_servers(cls, raw_value: Any):
        if not isinstance(raw_value, str):
            return raw_value
        if "[" in raw_value:
            return json.loads(raw_value)
        return [item.strip() for item in raw_value.split(",")]

    model_config = ConfigDict(extra="allow")
