import os
from textwrap import dedent

import pytest

from horizon.backend.settings import Settings


def _clear_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable_name in tuple(os.environ):
        if variable_name.startswith("HORIZON__"):
            monkeypatch.delenv(variable_name)


def test_settings_are_loaded_from_default_yaml_file(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    monkeypatch.delenv("HORIZON_CONFIG_FILE", raising=False)
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        dedent(
            """\
            admin_users:
              - yaml-admin
            database:
              url: "postgresql+asyncpg://user:password'#[value]@localhost:5432/horizon"
            server:
              debug: true
              cors:
                enabled: true
                allow_origins: ["*"]
                allow_credentials: true
                allow_methods: ["GET", "POST"]
                allow_headers: ["*"]
                expose_headers: ["X-Request-ID", "Location"]
            """,
        ),
        encoding="utf-8",
    )

    settings = Settings()

    assert settings.admin_users == ["yaml-admin"]
    assert settings.database.url == "postgresql+asyncpg://user:password'#[value]@localhost:5432/horizon"
    assert settings.server.debug is True
    assert settings.server.cors.dict() == {
        "enabled": True,
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["*"],
        "expose_headers": ["X-Request-ID", "Location"],
    }


def test_yaml_file_overrides_environment(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    config_path = tmp_path / "custom.yml"
    config_path.write_text(
        dedent(
            """\
            admin_users:
              - yaml-admin
            database:
              url: postgresql+asyncpg://yaml@localhost:5432/horizon
            server:
              debug: false
              cors:
                allow_origins: [https://yaml.example.com]
            """,
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("HORIZON_CONFIG_FILE", str(config_path))
    monkeypatch.setenv(
        "HORIZON__DATABASE__URL",
        "postgresql+asyncpg://env@localhost:5432/horizon",
    )
    monkeypatch.setenv("HORIZON__SERVER__DEBUG", "true")
    monkeypatch.setenv("HORIZON__ADMIN_USERS", '["env-admin"]')
    monkeypatch.setenv(
        "HORIZON__SERVER__CORS__ALLOW_ORIGINS",
        '["https://env.example.com"]',
    )

    settings = Settings()

    assert settings.admin_users == ["yaml-admin"]
    assert settings.database.url == "postgresql+asyncpg://yaml@localhost:5432/horizon"
    assert settings.server.debug is False
    assert settings.server.cors.allow_origins == ["https://yaml.example.com"]


def test_settings_can_be_loaded_from_environment_without_yaml_file(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_settings_environment(monkeypatch)
    monkeypatch.setenv("HORIZON_CONFIG_FILE", str(tmp_path / "missing.yml"))
    monkeypatch.setenv(
        "HORIZON__DATABASE__URL",
        "postgresql+asyncpg://env@localhost:5432/horizon",
    )
    monkeypatch.setenv("HORIZON__ADMIN_USERS", '["env-admin"]')

    settings = Settings()

    assert settings.admin_users == ["env-admin"]
    assert settings.database.url == "postgresql+asyncpg://env@localhost:5432/horizon"
