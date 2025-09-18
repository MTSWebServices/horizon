# Провайдеры аутентификации { #backend-auth-providers }

Horizon поддерживает различные реализации провайдеров аутентификации. Вы можете изменить реализацию через настройки:

::: horizon.backend.settings.auth.AuthSettings



# Провайдеры аутентификации

* [Фиктивный провайдер аутентификации][backend-auth-dummy]
   * [Описание](dummy.md#description)
   * [Схема взаимодействия](dummy.md#interaction-schema)
   * [Конфигурация](dummy.md#configuration)
* [LDAP провайдер аутентификации][backend-auth-ldap]
  * [Описание](ldap.md#description)
  * [Стратегии](ldap.md#strategies)
  * [Схема взаимодействия](ldap.md#interaction-schema)
  * [Базовая конфигурация](ldap.md#basic-configuration)
  * [Конфигурация, связанная с поиском](ldap.md#lookup-related-configuration)
* [Кешированный LDAP провайдер аутентификации][backend-auth-ldap-cached]
  * [Описание](cached_ldap.md#description)
  * [Схема взаимодействия](cached_ldap.md#interaction-schema)
  * [Конфигурация](cached_ldap.md#configuration)

# Для разработчиков

* [Пользовательский провайдер аутентификации][backend-auth-custom]

