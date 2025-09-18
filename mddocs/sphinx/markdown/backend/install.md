<a id="backend-install"></a>

# Install & run backend

## With docker

### Requirements

* [Docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://github.com/docker/compose/releases/)

### Installation process

Docker will download backend image of Horizon & Postgres, and run them.
Options can be set via `.env` file or `environment` section in `docker-compose.yml`

### `docker-compose.yml`

```default
services:
  db:
    image: postgres:17
    restart: unless-stopped
    environment:
      POSTGRES_DB: horizon
      POSTGRES_USER: horizon
      POSTGRES_PASSWORD: 123UsedForTestOnly
      POSTGRES_INITDB_ARGS: --encoding=UTF-8 --lc-collate=C --lc-ctype=C
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready
      start_period: 5s
      interval: 30s
      timeout: 5s
      retries: 3

  backend:
    image: mtsrus/horizon-backend:${VERSION:-latest}
    restart: unless-stopped
    env_file: .env.docker
    environment:
      # list here usernames which should be assigned SUPERADMIN role on application start
      HORIZON__ENTRYPOINT__ADMIN_USERS: admin
      # PROMETHEUS_MULTIPROC_DIR is required for multiple workers, see:
      # https://prometheus.github.io/client_python/multiprocess/
      PROMETHEUS_MULTIPROC_DIR: /tmp/prometheus-metrics
    # tmpfs dir is cleaned up each container restart
    tmpfs:
      - /tmp/prometheus-metrics:mode=1777
    ports:
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

### `.env.docker`

```default
# See Backend -> Configuration documentation
HORIZON__DATABASE__URL=postgresql+asyncpg://horizon:123UsedForTestOnly@db:5432/horizon
HORIZON__AUTH__PROVIDER=horizon.backend.providers.auth.dummy.DummyAuthProvider
HORIZON__AUTH__ACCESS_TOKEN__SECRET_KEY=234UsedForTestOnly
HORIZON__AUTH__LDAP__URL=ldap://ldap:389
HORIZON__AUTH__LDAP__BASE_DN=ou=people,dc=ldapmock,dc=local
HORIZON__AUTH__LDAP__LOOKUP__CREDENTIALS__USER=uid=adminuser1,ou=people,dc=ldapmock,dc=local
HORIZON__AUTH__LDAP__LOOKUP__CREDENTIALS__PASSWORD=password
HORIZON__SERVER__DEBUG=true
HORIZON__SERVER__LOGGING__PRESET=colored
HORIZON_TEST_SERVER_URL=http://backend:8000
HORIZON__SERVER__CORS__ENABLED=True
HORIZON__SERVER__CORS__ALLOW_ORIGINS=["http://localhost:3000"]
HORIZON__SERVER__CORS__ALLOW_CREDENTIALS=True
HORIZON__SERVER__CORS__ALLOW_METHODS=["*"]
HORIZON__SERVER__CORS__ALLOW_HEADERS=["*"]
HORIZON__SERVER__CORS__EXPOSE_HEADERS=["X-Request-ID","Location","Access-Control-Allow-Credentials"]
```

After container is started and ready, open [http://localhost:8000/docs](http://localhost:8000/docs).

Users listed in `HORIZON__ENTRYPOINT__ADMIN_USERS` env variable will be automatically promoted to `SUPERADMIN` role.

## Without docker

### Requirements

* Python 3.7 or above
* Pydantic 2.x
* `libldap2-dev`, `libsasl2-dev`, `libkrb5-dev` (for [LDAP Auth provider](auth/ldap.md#backend-auth-ldap))
* Some relation database instance, like [Postgres](https://www.postgresql.org/)

### Installation process

Install `data-horizon` package with following *extra* dependencies:

```console
$ pip install data-horizon[backend,postgres,ldap]
```

Available *extras* are:

* `backend` - main backend requirements, like FastAPI, SQLAlchemy and so on.
* `postgres` - requirements required to use Postgres as backend data storage.
* `ldap` - requirements used by [LDAP Auth provider](auth/ldap.md#backend-auth-ldap).

#### NOTE
For **macOS** users, an additional step is required. [You need to install the “bonsai” Python library from source code](https://bonsai.readthedocs.io/en/latest/install.html#install-from-source-on-macos). This installation is necessary to work with LDAP.

### Run database

Start Postgres instance somewhere, and set up database url using environment variables:

```bash
HORIZON__DATABASE__URL=postgresql+asyncpg://user:password@postgres-host:5432/database_name
```

You can use virtually any database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls),
but the only one we really tested is Postgres.

See [Database settings](configuration/database.md#backend-configuration-database) for more options.

### Run migrations

To apply migrations (database structure changes) you need to execute following command:

```console
$ python -m horizon.backend.db.migrations upgrade head
```

This is a thin wrapper around [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration) cli,
options and commands are just the same.

#### NOTE
This command should be executed after each upgrade to new Horizon version.

### Run backend

To start backend server you need to execute following command:

```console
$ python -m horizon.backend --host 0.0.0.0 --port 8000
```

This is a thin wrapper around [uvicorn](https://www.uvicorn.org/#command-line-options) cli,
options and commands are just the same.

After server is started and ready, open [http://localhost:8000/docs](http://localhost:8000/docs).

### Add admin users

To promote specific users to `SUPERADMIN` role, run the following script:

```console
$ python -m horizon.backend.scripts.manage_admins add admin1 admin2
```

See [Scripts](scripts/index.md#scripts) documentation.
