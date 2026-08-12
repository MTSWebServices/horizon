import pytest

from horizon.backend.settings import Settings


@pytest.fixture(scope="session", params=[{}])
def settings(request: pytest.FixtureRequest) -> Settings:
    return Settings.model_validate(request.param)
