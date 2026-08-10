# SPDX-FileCopyrightText: 2023-present MTS PJSC
# SPDX-License-Identifier: Apache-2.0

"""
Settings for LDAPAuthProvider class.

Basic LDAP terminology is explained here: `LDAP Overview <https://www.zytrax.com/books/ldap/ch2/>`_
"""

import textwrap
from typing import Annotated, Literal

from bonsai import LDAPSearchScope
from pydantic import AnyUrl, BaseModel, Field, SecretStr, UrlConstraints, field_validator

from horizon.backend.settings.auth.jwt import JWTSettings

LDAPUrl = Annotated[
    AnyUrl,
    UrlConstraints(allowed_schemes=["ldap", "ldaps"], host_required=True),
]


class LDAPCredentials(BaseModel):
    """LDAP lookup query is executed using this credentials
    (instead of login and password provided by user).

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      ldap:
        lookup:
          credentials:
            user: uid=techuser,ou=users,dc=example,dc=com
            password: somepassword
    ```
    """

    user: str = Field(
        description="DN of user which is used for calling ``lookup`` query in LDAP",
    )
    password: SecretStr = Field(
        description="This user password",
    )


class LDAPConnectionPoolSettings(BaseModel):
    """Settings related to LDAP connection pool.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      ldap:
        lookup:
          pool:
            enabled: true
            max: 10
    ```
    """

    enabled: bool = Field(
        default=True,
        description="Set to ``True`` to enable connection pool",
    )
    initial: int = Field(
        default=1,
        description="Initial size of connection pool",
    )
    max: int = Field(
        default=10,
        description="Maximum size of connection pool",
    )


class LDAPLookupSettings(BaseModel):
    """Settings related to LDAP lookup.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      ldap:
        lookup:
          enabled: true
          pool:
            enabled: true
          credentials:
            user: uid=techuser,ou=users,dc=example,dc=com
            password: somepassword
          query_template: (uid={login})
    ```
    """

    enabled: bool = Field(
        default=True,
        description="Set to ``True`` to enable lookup",
    )
    check_on_startup: bool = Field(
        default=True,
        description="If ``True``, and LDAP is not available during application start, abort application startup",
    )
    pool: LDAPConnectionPoolSettings = Field(
        default_factory=LDAPConnectionPoolSettings,
        description="LDAP connection pool settings",
    )
    credentials: LDAPCredentials | None = Field(
        default=None,
        description="Credentials used for connecting to LDAP while performing user lookup",
    )
    query_template: str = Field(
        default="({uid_attribute}={login})",
        description=textwrap.dedent(
            """
            LDAP query send in lookup request.

            Usually lookup is performed against attributes `uid` (LDAP) or `sAMAccountName` (ActiveDirectory).
            You can also pass any query string supported by LDAP.
            See [Bonsai documentation](https://bonsai.readthedocs.io/en/latest/tutorial.html#searching).

            Supported substitution values (see [horizon.backend.settings.auth.ldap.LDAPSettings][].):
              * `{uid_attribute}`
              * `{login}`
            """,
        ),
    )
    scope: LDAPSearchScope = Field(
        default=LDAPSearchScope.ONELEVEL,
        description=textwrap.dedent(
            """
            Lookup scope. Use `SUBTREE` for ActiveDirectory.

            See [Bonsai documentation](https://bonsai.readthedocs.io/en/latest/api.html#bonsai.LDAPSearchScope.ONE).
            """,
        ),
    )

    @field_validator("scope", mode="before")
    @classmethod
    def _convert_scope_to_enum(cls, value: str | int | LDAPSearchScope) -> LDAPSearchScope:
        if isinstance(value, str):
            return LDAPSearchScope[value.upper()]
        return LDAPSearchScope(value)


class LDAPSettings(BaseModel):
    """Settings related to LDAP interaction.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      ldap:
        url: ldap://ldap.domain.com:389
        base_dn: ou=users,dc=example,dc=com
        uid_attribute: sAMAccountName
    ```
    """

    url: LDAPUrl = Field(
        description="LDAP URL to connect to",
    )
    timeout_seconds: int | None = Field(
        default=10,
        description="LDAP request timeout, in seconds. ``None`` means no timeout",
    )
    auth_mechanism: Literal["SIMPLE", "DIGEST-MD5"] = Field(
        default="SIMPLE",
        description="LDAP auth mechanism, used for ``bind`` request",
    )
    base_dn: str = Field(
        description="Organization DN, e.g. ``ou=users,dc=example,dc=com``",
    )
    uid_attribute: str = Field(
        default="uid",
        description=textwrap.dedent(
            """
            Attribute containing username.

            Usually `uid` (LDAP) or `sAMAccountName` (ActiveDirectory).
            """,
        ),
    )
    bind_dn_template: str = Field(
        default="{uid_attribute}={login},{base_dn}",
        description=textwrap.dedent(
            """
            Template for building DN string, used for checking credentials in LDAP.
            You can pass any DN value supported by LDAP.

            Supported substitution values:
              * `{login}`
              * `{uid_attribute}` (see [uid_attribute][])
              * `{base_dn}` (see [base_dn][])
            """,
        ),
    )

    lookup: LDAPLookupSettings = Field(
        default_factory=LDAPLookupSettings,
        description="LDAP search options",
    )


class LDAPAuthProviderSettings(BaseModel):
    """Settings for LDAPAuthProvider.

    Examples
    --------

    ```yaml title="config.yml"
    auth:
      provider: horizon.backend.providers.auth.ldap.LDAPAuthProvider
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
    ```
    """

    access_token: JWTSettings = Field(description="Access-token related settings")
    ldap: LDAPSettings = Field(description="LDAP related settings")
