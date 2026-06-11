# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

import textwrap
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from typing_extensions import Literal

LOG_PATH = Path(__file__).parent.resolve()


class LoggingSettings(BaseModel):
    """Logging Settings.

    Examples
    --------

    Using `json` preset:

    ```bash
    HORIZON__SERVER__LOGGING__SETUP=True
    HORIZON__SERVER__LOGGING__PRESET=json
    ```
    Passing custom logging config file:

    ```bash
    HORIZON__SERVER__LOGGING__SETUP=True
    HORIZON__SERVER__LOGGING__CUSTOM_CONFIG_PATH=/some/logging.yml
    ```
    Setup logging in some other way, e.g. using [uvicorn args](https://www.uvicorn.org/settings/#logging):

    ```bash
    $ export HORIZON__SERVER__LOGGING__SETUP=False
    $ python -m horizon.backend --log-level debug
    ```
    """

    setup: bool = Field(
        default=True,
        description="If `True`, setup logging during application start",
    )
    preset: Literal["json", "plain", "colored"] = Field(
        default="plain",
        description=textwrap.dedent(
            """
            Name of logging preset to use.

            There are few logging presets bundled to `data-horizon[backend]` package:

            ??? note "`plain` preset"

                This preset is recommended to use in environment which do not support colored output,
                e.g. CI jobs

                --8<--
                horizon/backend/settings/server/log/plain.yml
                --8<--

            ??? note "`colored` preset"

                This preset is recommended to use in development environment,
                as it simplifies debugging. Each log record is output with color specific for a log level

                --8<--
                horizon/backend/settings/server/log/colored.yml
                --8<--

            ??? note "`json` preset"

                This preset is recommended to use in production environment,
                as it allows to avoid writing complex log parsing configs. Each log record is output as JSON line

                --8<--
                horizon/backend/settings/server/log/json.yml
                --8<--
            """,
        ),
    )

    custom_config_path: Optional[Path] = Field(
        default=None,
        description=textwrap.dedent(
            """
            Path to custom logging configuration file. If set, overrides [preset][] value.

            File content should be in YAML format and conform
            [logging.dictConfig](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema).
            """,
        ),
    )

    def get_log_config_path(self) -> Path:
        return self.custom_config_path or LOG_PATH / f"{self.preset}.yml"
