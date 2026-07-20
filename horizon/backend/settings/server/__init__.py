# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

import textwrap

from pydantic import BaseModel, Field

from horizon.backend.settings.server.application_version import (
    ApplicationVersionSettings,
)
from horizon.backend.settings.server.cors import CORSSettings
from horizon.backend.settings.server.log import LoggingSettings
from horizon.backend.settings.server.monitoring import MonitoringSettings
from horizon.backend.settings.server.openapi import OpenAPISettings
from horizon.backend.settings.server.request_id import RequestIDSettings
from horizon.backend.settings.server.static_files import StaticFilesSettings


class ServerSettings(BaseModel):
    """Backend server settings.

    Examples
    --------

    ```yaml title="config.yml"
    server:
      debug: true
      logging:
        preset: colored
      monitoring:
        enabled: true
      cors:
        enabled: true
      request_id:
        enabled: true
      openapi:
        enabled: true
        swagger:
          enabled: true
        redoc:
          enabled: true
    ```
    """

    debug: bool = Field(
        default=False,
        description=textwrap.dedent(
            """
            [Enable debug output in responses][backend-configuration-debug].
            Do not use this on production!
            """,
        ),
    )
    logging: LoggingSettings = Field(
        default_factory=LoggingSettings,
        description="[Logging settings][backend-configuration-logging]",
    )
    cors: CORSSettings = Field(
        default_factory=CORSSettings,
        description="[CORS settings][backend-configuration-cors]",
    )
    monitoring: MonitoringSettings = Field(
        default_factory=MonitoringSettings,
        description="[Monitoring settings][backend-configuration-monitoring]",
    )
    request_id: RequestIDSettings = Field(
        default_factory=RequestIDSettings,
        description="[RequestID settings][backend-configuration-debug]",
    )
    application_version: ApplicationVersionSettings = Field(
        default_factory=ApplicationVersionSettings,
        description="[Application version settings][backend-configuration-debug]",
    )
    static_files: StaticFilesSettings = Field(
        default_factory=StaticFilesSettings,
        description="[Static files settings][backend-configuration-static-files]",
    )
    openapi: OpenAPISettings = Field(
        default_factory=OpenAPISettings,
        description="[OpenAPI.json settings][backend-configuration-openapi]",
    )
