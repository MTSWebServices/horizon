# Auth Providers { #backend-auth-providers }

Horizon supports different auth provider implementations. You can change implementation via settings:

::: horizon.backend.settings.auth.AuthSettings

## Auth providers

* [Dummy Auth provider][backend-auth-dummy]
  * [Description][dummy-description]
  * [Interaction schema][dummy-interaction-schema]
  * [Configuration][dummy-configuration]
* [LDAP Auth provider][backend-auth-ldap]
  * [Description][ldap-description]
  * [Strategies][ldap-strategies]
  * [Interaction schema][ldap-interaction-schema]
  * [Basic configuration][ldap-basic-configuration]
  * [Lookup-related configuration][ldap-lookup-related-configuration]
* [LDAP Cached Auth provider][backend-auth-ldap-cached]
  * [Description][cached_ldap-description]
  * [Interaction schema][cached_ldap-interaction-schema]
  * [Configuration][cached_ldap-configuration]

## For developers

* [Custom Auth provider][backend-auth-custom]
