# Configuration { #backend-configuration }

Horizon reads application settings from `config.yml` in the current working directory.
Use `HORIZON_CONFIG_FILE` to point to another YAML file.

```yaml title="config.yml"
admin_users:
  - admin

database:
  url: postgresql+asyncpg://user:password@localhost:5432/horizon

server:
  debug: true
  cors:
    enabled: true
    allow_origins: ["*"]
```

Every setting can also be passed through an environment variable. Environment variable
names are prefixed with `HORIZON__`, and nested keys are separated with `__`.

```bash title="Environment variables"
export HORIZON__DATABASE__URL=postgresql+asyncpg://user:password@localhost:5432/horizon
export HORIZON__ADMIN_USERS='["admin"]'
export HORIZON__SERVER__DEBUG=true
export HORIZON__SERVER__CORS__ENABLED=true
export HORIZON__SERVER__CORS__ALLOW_ORIGINS='["*"]'
```

Values loaded from the YAML file override values passed through environment variables.
Settings passed directly to the `Settings` constructor have the highest priority.

* [Database][backend-configuration-database]
* [Logging][backend-configuration-logging]
* [Monitoring][backend-configuration-monitoring]
* [CORS][backend-configuration-cors]
* [Static_files][backend-configuration-static-files]
* [Openapi][backend-configuration-openapi]
* [Debug][backend-configuration-debug]

::: horizon.backend.settings
    options:
        members:
            - Settings
            - server
                - ServerSettings
