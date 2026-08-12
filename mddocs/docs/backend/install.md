# Install & run backend { #backend-install }

## With docker

### Requirements

- [Docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://github.com/docker/compose/releases/)

### Installation process

Docker will download backend image of Horizon & Postgres, and run them.
Application settings are loaded from `config.docker.yml`.
Settings omitted from the YAML file can be passed through the `environment` section in `docker-compose.yml`.

### `docker-compose.yml`

```yaml
--8<--
docker-compose.yml
--8<--
```

### `config.docker.yml`

```yaml
--8<--
config.docker.yml
--8<--
```

After container is started and ready, open [http://localhost:8000/docs](http://localhost:8000/docs).

Users listed in the `admin_users` configuration field are automatically promoted to the `SUPERADMIN` role.

## Without docker

### Requirements without docker

- Python 3.10 or above
- Pydantic 2.x
- `libldap2-dev`, `libsasl2-dev`, `libkrb5-dev` (for [LDAP Auth provider][backend-auth-ldap])
- Some relation database instance, like [Postgres](https://www.postgresql.org/)

### Installation process without docker

Install `data-horizon` package with following *extra* dependencies:

```console
$ pip install data-horizon[backend,postgres,ldap]
...
```

Available *extras* are:

- `backend` - main backend requirements, like FastAPI, SQLAlchemy and so on.
- `postgres` - requirements required to use Postgres as backend data storage.
- `ldap` - requirements used by [LDAP Auth provider][backend-auth-ldap].

!!! note
    For **macOS** users, an additional step is required. [You need to install the “bonsai” Python library from source code](https://bonsai.readthedocs.io/en/latest/install.html#install-from-source-on-macos). This installation is necessary to work with LDAP.

### Run database

Start Postgres instance somewhere, and set up the database URL in `config.yml`:

```yaml
database:
  url: postgresql+asyncpg://user:password@postgres-host:5432/database_name
```

You can use virtually any database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls),
but the only one we really tested is Postgres.

If the value is omitted from `config.yml`, it can be passed using an environment variable:

```bash
export HORIZON__DATABASE__URL=postgresql+asyncpg://user:password@postgres-host:5432/database_name
```

See [Database settings][backend-configuration-database] for more options.

### Run migrations

To apply migrations (database structure changes) you need to execute following command:

```console
$ python -m horizon.backend.db.migrations upgrade head
...
```

This is a thin wrapper around [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration) cli,
options and commands are just the same.

!!! note "run migrations"
    This command should be executed after each upgrade to new Horizon version.

### Run backend

To start backend server you need to execute following command:

```console
$ python -m horizon.backend --host 0.0.0.0 --port 8000
...
```

This is a thin wrapper around [uvicorn](https://www.uvicorn.org/#command-line-options) cli,
options and commands are just the same.

After server is started and ready, open [http://localhost:8000/docs](http://localhost:8000/docs).

### Add admin users

List users which should automatically receive the `SUPERADMIN` role in `config.yml`:

```yaml
admin_users:
  - admin1
  - admin2
```

Then run the following script without arguments, or pass usernames explicitly:

```console
$ python -m horizon.backend.scripts.manage_admins add
$ python -m horizon.backend.scripts.manage_admins add admin1 admin2
...
```

See [Scripts][scripts] documentation.
