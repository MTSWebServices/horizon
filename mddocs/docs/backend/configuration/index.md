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

::: horizon.backend.settings
    options:
        show_root_heading: false
        members:
            - Settings

::: horizon.backend.settings.server
    options:
        show_root_heading: false
        members:
              - ServerSettings
