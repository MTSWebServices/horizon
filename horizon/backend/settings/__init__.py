# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path
from typing import Any

import yaml
from fastapi import Request
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from horizon.backend.settings.auth import AuthSettings
from horizon.backend.settings.database import DatabaseSettings
from horizon.backend.settings.server import ServerSettings


def _read_yaml_config() -> dict[str, Any]:
    config_path = Path(os.getenv("HORIZON_CONFIG_FILE", "config.yml"))
    if not config_path.is_file():
        return {}

    with config_path.open(encoding="utf-8") as config_file:
        config: dict[str, Any] = yaml.safe_load(config_file) or {}

    return config


class Settings(BaseSettings):
    """Horizon backend settings.

    Backend can be configured in 3 ways, in descending order of priority:

    * By explicitly passing `settings` object as an argument to `application_factory`
    * By storing settings in a `config.yml` configuration file
    * By setting environment variables matching a specific key

    Environment variable names are written in uppercase, prefixed with `HORIZON__`,
    and use `__` to delimit nested items.

    More details can be found in [Pydantic documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

    Examples
    --------

    ```yaml title="config.yml"
    database:
      url: postgresql+asyncpg://postgres:postgres@localhost:5432/horizon

    server:
      debug: true

    auth:
      provider: horizon.backend.providers.auth.dummy.DummyAuthProvider

    admin_users:
      - admin
    ```
    """

    model_config = SettingsConfigDict(
        env_prefix="HORIZON__",
        env_nested_delimiter="__",
    )

    admin_users: list[str] = Field(
        default_factory=list,
        description="Usernames which should be assigned SUPERADMIN role on application start",
    )
    database: DatabaseSettings = Field(description="[Database settings][backend-configuration-database]")
    server: ServerSettings = Field(
        default_factory=ServerSettings,
        description="[Server settings][backend-configuration]",
    )
    auth: AuthSettings = Field(
        default_factory=AuthSettings,
        description="[Auth setting][backend-auth-providers]",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Any,
        init_settings: Any,
        env_settings: Any,
        dotenv_settings: Any,
        file_secret_settings: Any,
    ) -> tuple[Any, ...]:
        return (
            init_settings,
            _read_yaml_config,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


async def get_settings(request: Request) -> Settings:
    return request.app.state.settings
