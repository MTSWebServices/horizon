#!make

include .env.local.test

HORIZON_CONFIG_FILE ?= config.yml
export HORIZON_CONFIG_FILE

VERSION := $(shell cat horizon/VERSION)
DATE := $(shell date --rfc-3339=date)

VIRTUAL_ENV ?= .venv
PYTHON = ${VIRTUAL_ENV}/bin/python
PIP = ${VIRTUAL_ENV}/bin/pip
UV ?= ${VIRTUAL_ENV}/bin/uv
PYTEST = ${VIRTUAL_ENV}/bin/pytest

# Fix docker build and docker compose build using different backends
COMPOSE_DOCKER_CLI_BUILD = 1
DOCKER_BUILDKIT = 1
# Fix docker build on M1/M2
DOCKER_DEFAULT_PLATFORM = linux/amd64

export DISABLE_MKDOCS_2_WARNING=true

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

all: help

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)



venv: venv-cleanup  venv-install##@Env Init venv and install dependencies

venv-cleanup: ##@Env Cleanup venv
	@rm -rf ${VIRTUAL_ENV} || true
	python3 -m venv ${VIRTUAL_ENV}
	${PIP} install uv

venv-install: ##@Env Install requirements to venv
	${UV} sync --inexact --frozen --all-extras --all-groups $(ARGS)



db: db-start db-upgrade ##@DB Prepare database (in docker)

db-start: ##@DB Start database
	docker compose -f docker-compose.test.yml up -d --wait db $(DOCKER_COMPOSE_ARGS)

db-revision: ##@DB Generate migration file
	${PYTHON} -m horizon.backend.db.migrations revision --autogenerate

db-upgrade: ##@DB Run migrations to head
	${PYTHON} -m horizon.backend.db.migrations upgrade head

db-downgrade: ##@DB Downgrade head migration
	${PYTHON} -m horizon.backend.db.migrations downgrade head-1

ldap-start: ##@LDAP Start LDAP container
	docker compose -f docker-compose.test.yml up -d --wait ldap $(DOCKER_COMPOSE_ARGS)


test: db ldap-start ##@Test Run tests
	${PYTEST} $(PYTEST_ARGS)

test-check-fixtures: ##@Test Check declared fixtures
	${PYTEST} --dead-fixtures $(PYTEST_ARGS)

test-cleanup: ##@Test Cleanup tests dependencies
	docker compose -f docker-compose.test.yml down $(ARGS)



dev: db-start ##@Application Run development server (without docker)
	${PYTHON} -m horizon.backend $(ARGS)

prod-build: ##@Application Build docker image
	docker build --progress=plain --network=host -t mtsrus/horizon-backend:latest -f ./docker/Dockerfile.backend --target prod $(ARGS) .

prod: ##@Application Run production server (with docker)
	docker compose up -d $(ARGS)

prod-cleanup: ##@Application Stop production server
	docker compose down --remove-orphans $(ARGS)


.PHONY: docs

docs: docs-build docs-open ##@Docs Generate & open docs

docs-build: ##@Docs Generate docs
	PYTHONPATH=. ${VIRTUAL_ENV}/bin/mkdocs build --config-file mddocs/mkdocs.yml

docs-open: ##@Docs Open docs
	xdg-open mddocs/generated/index.html

docs-cleanup: ##@Docs Cleanup docs
	rm -rf mddocs/generated/

docs-fresh: docs-cleanup docs-build ##@Docs Cleanup & build docs

docs-serve: ##@Docs Run docs server
	PYTHONPATH=. ${VIRTUAL_ENV}/bin/mkdocs serve --config-file mddocs/mkdocs.yml

docs-generate-changelog: ##@Docs Generate changelog
	echo "Building changelog for ${VERSION}"
	cp "mddocs/docs/changelog/RELEASE_TEMPLATE.md" "mddocs/docs/changelog/temp_RELEASE_TEMPLATE.md"
	${UV} run towncrier build "--version=${VERSION}" --yes
	mv "mddocs/docs/changelog/RELEASE_TEMPLATE.md" "mddocs/docs/changelog/${VERSION}.md"
	mv "mddocs/docs/changelog/temp_RELEASE_TEMPLATE.md" "mddocs/docs/changelog/RELEASE_TEMPLATE.md"

	# Remove content above the version number heading in the `${VERSION}.md` file
	awk '!/towncrier release notes start/' "mddocs/docs/changelog/${VERSION}.md" | sed '/./,$$!d' > temp && mv temp "mddocs/docs/changelog/${VERSION}.md"

	# Update Changelog Index and Navigation
	sed "s#\(.*NEXT_RELEASE.*\)#\1\n- [${VERSION} (${DATE})][${VERSION}]#" "mddocs/docs/changelog/index.md" > temp && mv temp "mddocs/docs/changelog/index.md"
	sed "s#\(.*NEXT_RELEASE.*\)#\1\n    * [${VERSION}](changelog/${VERSION}.md)#" "mddocs/docs/nav.md" > temp && mv temp "mddocs/docs/nav.md"

docs-openapi: ##@Docs Generate OpenAPI schema
	${PYTHON} -m horizon.backend.export_openapi_schema mddocs/docs/_static/openapi.json
