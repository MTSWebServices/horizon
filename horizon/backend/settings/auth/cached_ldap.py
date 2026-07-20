# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

"""
Settings for LDAPAuthProvider class.

Basic LDAP terminology is explained here: `LDAP Overview <https://www.zytrax.com/books/ldap/ch2/>`_
"""

import textwrap
from typing import Any, Dict

from pydantic import BaseModel, Field

from horizon.backend.settings.auth.ldap import LDAPAuthProviderSettings


class LDAPCachePasswordHashSettings(BaseModel):
    """Settings related to LDAP credentials cache password hashing.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      cache:
        password_hash:
          algorithm: argon2
          options:
            time_cost: 2
            memory_cost: 1024
            parallelism: 1
    ```
    """

    algorithm: str = Field(
        default="argon2",
        description=textwrap.dedent(
            """
            Hashing algorithm used to hash user credentials.

            See [passlib documentation](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.html#active-hashes)
            for more details.
            """,
        ),
    )
    options: Dict[str, Any] = Field(
        default={},
        description="Options passed to hashing algorithm",
    )


class LDAPCacheSettings(BaseModel):
    """Settings related to LDAP credentials cache.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      cache:
        expire_seconds: 3600  # 1 hour
    ```
    """

    expire_seconds: int = Field(
        default=60 * 60,
        description=textwrap.dedent(
            """
            Credentials cache expiration time, in seconds.

            !!! warning

                Please do not set too large value here, as it may lead to security issues.
            """,
        ),
    )
    password_hash: LDAPCachePasswordHashSettings = Field(
        default_factory=LDAPCachePasswordHashSettings,
        description="Password hashing options",
    )


class CachedLDAPAuthProviderSettings(LDAPAuthProviderSettings):
    """Settings for CachedLDAPAuthProvider.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      provider: horizon.backend.providers.auth.cached_ldap.CachedLDAPAuthProvider
      access_token:
        secret_key: secret
      ldap:
        url: ldap://ldap.domain.com:389
        base_dn: ou=users,dc=example,dc=com
        lookup:
          enabled: true
          pool:
            enabled: true
          credentials:
            user: uid=techuser,ou=users,dc=example,dc=com
            password: somepassword
      cache:
        expire_seconds: 3600  # 1 hour
    ```
    """

    cache: LDAPCacheSettings = Field(default_factory=LDAPCacheSettings, description="Cache related settings")
