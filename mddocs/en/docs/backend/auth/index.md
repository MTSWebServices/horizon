# Auth Providers { #backend-auth-providers }

Horizon supports different auth provider implementations. You can change implementation via settings:

::: horizon.backend.settings.auth.AuthSettings

## Auth providers

* [Dummy Auth provider][backend-auth-dummy]
  * [Description](dummy.md#description)
  * [Interaction schema](dummy.md#interaction-schema)
  * [Configuration](dummy.md#configuration)
* [LDAP Auth provider][backend-auth-ldap]
  * [Description](ldap.md#description)
  * [Strategies](ldap.md#strategies)
  * [Interaction schema](ldap.md#interaction-schema)
  * [Basic configuration](ldap.md#basic-configuration)
  * [Lookup-related configuration](ldap.md#lookup-related-configuration)
* [LDAP Cached Auth provider][backend-auth-ldap-cached]
  * [Description](cached_ldap.md#description)
  * [Interaction schema](cached_ldap.md#interaction-schema)
  * [Configuration](cached_ldap.md#configuration)

## For developers

* [Custom Auth provider][backend-auth-custom]
