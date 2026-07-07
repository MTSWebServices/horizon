# Data.Horizon { #readme }

[![Repo status - Active](https://www.repostatus.org/badges/latest/active.svg)](https://github.com/MTSWebServices/horizon) [![DockerHub - Latest release](https://img.shields.io/docker/v/mtsrus/horizon-backend?sort=semver&label=docker)](https://hub.docker.com/r/mtsrus/horizon-backend) [![PyPI - Latest Release](https://img.shields.io/pypi/v/data-horizon)](https://pypi.org/project/data-horizon/) [![PyPI - License](https://img.shields.io/pypi/l/data-horizon.svg)](https://github.com/MTSWebServices/horizon/blob/develop/LICENSE.txt) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/data-horizon.svg)](https://pypi.org/project/data-horizon/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/data-horizon)](https://pypi.org/project/data-horizon/)
[![Documentation - ReadTheDocs](https://readthedocs.org/projects/data-horizon/badge/?version=stable)](https://data-horizon.readthedocs.io/) [![Github Actions - latest CI build status](https://github.com/MTSWebServices/horizon/workflows/Tests/badge.svg)](https://github.com/MTSWebServices/horizon/actions) [![Test coverage - percent](https://codecov.io/gh/MobileTeleSystems/horizon/branch/develop/graph/badge.svg?token=BIRWPTWEE0)](https://codecov.io/gh/MobileTeleSystems/horizon) [![pre-commit.ci - status](https://results.pre-commit.ci/badge/github/MobileTeleSystems/horizon/develop.svg)](https://results.pre-commit.ci/latest/github/MobileTeleSystems/horizon/develop)

![Horizon logo](_static/logo.svg){class="readme-logo"}

## What is Data.Horizon?

Data.Horizon is an application that implements simple HWM Store. Right now it includes:

* REST API
* Python client

## Goals

* Allow users to save and fetch High Water Mark (*HWM*) items. These are `name+type+value` triples with few optional fields.
* Avoid confusion between different user’s data by separating HWMs to different *namespaces*. Each HWM is bound to namespace.
* Allow users to get HWM change history, to determine who and when changed a specific HWM value and other fields.
* Provide RBAC model to ensure that interaction with `HWMs` and `Namespaces` are governed by role assigned to each user. Roles are assigned per namespace.

## Non-goals

* This is not a *data* storage, it is not designed to store raw table rows. It is designed to store only HWM values.
* Attaching machine-readable metadata for HWMs (like `process`, `origin`) is not supported. This should be stored somewhere else.

## Horizon

High-level design

* [Entities][entities]
* [Permissions][permissions]

Backend

* [Install & run][backend-install]
* [Architecture][backend-architecture]
* [Configuration][backend-configuration]
* [Auth Providers][backend-auth-providers]
* [OpenAPI specification][backend-openapi]
* [Scripts][scripts]

Client

* [Install][client-install]
* [Sync client][client-sync]
* [Auth][client-auth]
* [Schemas][client-schemas-root]
* [Exceptions][client-exceptions]

Development

* [Changelog][changelog]
* [Contributing][contributing]
* [Security][security]
