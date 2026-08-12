Contributing Guide
==================

Welcome! There are many ways to contribute, including submitting bug
reports, improving documentation, submitting feature requests, reviewing
new submissions, or contributing code that can be incorporated into the
project.

Review process
--------------

For any **significant** changes please create a new GitHub issue and
enhancements that you wish to make. Describe the feature you would like
to see, why you need it, and how it will work. Discuss your ideas
transparently and get community feedback before proceeding.

Small changes can directly be crafted and submitted to the GitHub
Repository as a Pull Request. This requires creating a **repo fork** using
`instruction <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_.

Important notes
---------------

* Some companies still use Python 3.10. So it is required to keep compatibility if possible, at least for *client* part of package.
* Different users uses Horizon in different ways - someone store data in Postgres, someone in MySQL, some users need LDAP. Such dependencies should be optional.

Initial setup for local development
-----------------------------------

Install Git
~~~~~~~~~~~

Please follow `instruction <https://docs.github.com/en/get-started/quickstart/set-up-git>`_.

Clone the repo
~~~~~~~~~~~~~~

Open terminal and run these commands to clone a **forked** repo:

.. code:: bash

    git clone git@github.com:myuser/horizon.git -b develop

    cd horizon

Setup environment
~~~~~~~~~~~~~~~~~

Firstly, install `make <https://www.gnu.org/software/make/manual/make.html>`_. It is used for running complex commands in local environment.

Secondly, create virtualenv and install dependencies:

.. code:: bash

    make venv-init

If you already have venv, but need to install dependencies required for development:

.. code:: bash

    make venv-install

We are using `uv https://docs.astral.sh/uv/`_ for managing dependencies and building the package.
It allows to keep development environment the same for all developers due to using lock file with fixed dependency versions.

There are *extra* dependencies (included into package as optional):

* ``backend``
* ``client-sync``
* ``postgres``
* ``ldap``

And *groups* (not included into package, used locally and in CI):

* ``test`` - for running tests
* ``dev`` - for development, like linters, formatters, mypy, prek and so on
* ``docs`` - for building documentation

Enable pre-commit hooks
~~~~~~~~~~~~~~~~~~~~~~~

`pre-commit <https://pre-commit.com/>`_ hooks allows to validate & fix repository content before making new commit.
It allows to run linters, formatters, fix file permissions and so on. If something is wrong, changes cannot be committed.

Firstly, install `prek <https://prek.j178.dev/>`_:

.. code:: bash

    prek install --install-hooks

Ant then test hooks run:

.. code:: bash

    prek run

How to
------

Run development instance locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start DB container:

.. code:: bash

    make db

Then start development server:

.. code:: bash

    make dev

And open http://localhost:8000/docs

Application settings are stored in ``config.yml``. The ``.env.local.test`` file contains
test-only environment variables.

Working with migrations
~~~~~~~~~~~~~~~~~~~~~~~

Start database:

.. code:: bash

    make db-start

Generate revision:

.. code:: bash

    make db-revision

Upgrade db to ``head`` migration:

.. code:: bash

    make db-upgrade

Downgrade db to ``head-1`` migration:

.. code:: bash

    make db-downgrade

Run tests locally
~~~~~~~~~~~~~~~~~

Start all containers with dependencies:

.. code:: bash

    make db  # for backend & client tests
    make ldap-start  # for backend tests
    make dev  # for client test, run in separate terminal tab

Run tests:

.. code:: bash

    make test

You can pass additional arguments, they will be passed to pytest:

.. code:: bash

    make test PYTEST_ARGS="-m client-sync -lsx -vvvv --log-cli-level=INFO"

Stop all containers and remove created volumes:

.. code:: bash

    make cleanup ARGS="-v"

Get fixtures not used by any test:

.. code:: bash

    make check-fixtures

Build CI image locally
~~~~~~~~~~~~~~~~~~~~~~~~

This image is build in CI for testing purposes, but you can do that locally as well:

.. code:: bash

    make test-build

Run production instance locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, build production image:

.. code:: bash

    make prod-build

And then start it:

.. code:: bash

    make prod

Then open http://localhost:8000/docs

Application settings are stored in ``config.docker.yml``. The ``.env.docker.test``
file contains test-only variables.

Build documentation
~~~~~~~~~~~~~~~~~~~

Build documentation using mkdocs:

.. code:: bash

    make docs-serve

Then open in browser ``http://localhost:8000/``.

Create pull request
~~~~~~~~~~~~~~~~~~~

Commit your changes:

.. code:: bash

    git commit -m "Commit message"
    git push

Then open Github interface and `create pull request <https://docs.github.com/en/get-started/quickstart/contributing-to-projects#making-a-pull-request>`_.
Please follow guide from PR body template.

After pull request is created, it get a corresponding number, e.g. 123 (``pr_number``).

Write release notes
~~~~~~~~~~~~~~~~~~~

``Horizon`` uses `towncrier <https://pypi.org/project/towncrier/>`_
for changelog management.

To submit a change note about your PR, add a text file into the
`mddocs/docs/changelog/next_release <./next_release>`_ folder. It should contain an
explanation of what applying this PR will change in the way
end-users interact with the project. One sentence is usually
enough but feel free to add as many details as you feel necessary
for the users to understand what it means.

**Use the past tense** for the text in your fragment because,
combined with others, it will be a part of the "news digest"
telling the readers **what changed** in a specific version of
the library *since the previous version*.

Finally, name your file following the convention that Towncrier
understands: it should start with the number of an issue or a
PR followed by a dot, then add a patch type, like ``feature``,
``doc``, ``misc`` etc., and add ``.md`` as a suffix. If you
need to add more than one fragment, you may add an optional
sequence number (delimited with another period) between the type
and the suffix.

In general the name will follow ``<pr_number>.<category>.md`` pattern,
where the categories are:

- ``feature``: Any new feature. Adding new functionality that has not yet existed.
- ``removal``: Signifying a deprecation or removal of public API.
- ``bugfix``: A bug fix.
- ``improvement``: An improvement. Improving functionality that already existed.
- ``doc``: A change to the documentation.
- ``dependency``: Indicates that there have been changes in dependencies.
- ``misc``: Changes internal to the repo like CI, test and build changes.
- ``breaking``: introduces a breaking API change.
- ``significant``: Indicates that significant changes have been made to the code.

A pull request may have more than one of these components, for example
a code change may introduce a new feature that deprecates an old
feature, in which case two fragments should be added. It is not
necessary to make a separate documentation fragment for documentation
changes accompanying the relevant code changes.

Examples for adding changelog entries to your Pull Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: markdown
    :caption: mddocs/docs/changelog/next_release/2345.bugfix.md

    Fixed behavior of `backend`

.. code-block:: markdown
    :caption: mddocs/docs/changelog/next_release/3456.feature.md

    Added support of `timeout` in `LDAP`

.. tip::

    See `pyproject.toml <pyproject.toml>`_ for all available categories
    (``tool.towncrier.type``).

.. _Towncrier philosophy:
    https://towncrier.readthedocs.io/en/stable/#philosophy

How to skip change notes check?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just add ``ci:skip-changelog`` label to pull request.

Release Process
---------------

.. note::

    This is for repo maintainers only

Before making a release from the ``develop`` branch, follow these steps:

1. Checkout to ``develop`` branch and update it to the actual state

.. code:: bash

    git checkout develop
    git pull -p

2. Get current release version

.. code:: bash

    VERSION=$(cat horizon/VERSION)

3. Build changelog for current release

.. code:: bash

    make docs-generate-changelog

4. Commit and push changes to ``develop`` branch

.. code:: bash

    git add .
    git commit -m "Prepare for release ${VERSION}"
    git push

5. Merge ``develop`` branch to ``master``, **WITHOUT** squashing

.. code:: bash

    git checkout master
    git pull
    git merge develop
    git push

6. Add git tag to the latest commit in ``master`` branch

.. code:: bash

    git tag "$VERSION"
    git push origin "$VERSION"

7. Update version in ``develop`` branch **after release**:

.. code:: bash

    git checkout develop

    NEXT_VERSION=$(echo "$VERSION" | awk -F. '/[0-9]+\./{$NF++;print}' OFS=.)
    echo $NEXT_VERSION > horizon/VERSION

    git add .
    git commit -m "Bump version"
    git push
