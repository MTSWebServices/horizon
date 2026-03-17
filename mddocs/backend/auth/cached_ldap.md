# LDAP Cached Auth provider { #backend-auth-ldap-cached }

## Description { #cached_ldap-description }

Same as [LDAP Auth provider][backend-auth-ldap-cached], but if LDAP request for checking user credentials was successful,
credentials are stored in local cache (table in internal database, in form `login` + `hash(password)` + `update timestamp`).

Next auth requests for the same login are performed against this cache **first**. LDAP requests are send *only* if cache have been expired.

This allows to:

- Bypass errors with LDAP availability, e.g. network errors
- Reduce number of requests made to LDAP.

Downsides:

- If user changed password, and cache is not expired yet, user may still log in with old credentials.
- Same if user was blocked in LDAP.

## Interaction schema { #cached_ldap-interaction-schema }

```mermaid
sequenceDiagram
participant "Client"
participant "Backend"
participant "LDAP"

activate "Client"
alt First time auth | Empty cache | Cache expired
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Search for credentials cache by login
"Backend" ->> "Backend" : No items found or item expired, using LDAP
"Backend" ->> "Backend" : DN = bind_dn_template(login)
"Backend" ->> "LDAP"  : Call bind(DN, password)
"LDAP" ->> "Backend" : Successful
"Backend" ->> "Backend" : Check user in internal backend database,\nusername = login
"Backend" ->> "Backend" : Create user if not exist
"Backend" ->> "Backend" : Save credentials to cache
"Backend" ->> "Client"  : Generate and return access_token

else Using cache, LDAP is totally ignored
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Search for credentials cache by login
"Backend" ->> "Backend" : Found credentials, check for expiration
"Backend" ->> "Backend" : Not expired, validate password is matching hash
"Backend" ->> "Backend" : Password match, not calling LDAP
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" ->> "Backend" : Create user if not exist
"Backend" ->> "Client"  : Generate and return access_token

else Password mismatch with cache, LDAP is totally ignored
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Search for credentials cache by login
"Backend" ->> "Backend" : Found credentials, check for expiration
"Backend" ->> "Backend" : Not expired, validate password is matching hash
"Backend" ->> "Backend" : Password do not match local cache
"Backend" --x "Client"  : 401 Unauthorized

else No cache or cache expired, LDAP is unavailable
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Search for credentials cache by login
"Backend" ->> "Backend" : No items found or item expired, using LDAP
"Backend" ->> "Backend" : DN = bind_dn_template(login)
"Backend" --x "LDAP" : Call bind(DN, password)
"Backend" --x "Client"  : 503 Service unavailable

else
Note right of "Client" : Other cases are same as for LDAPAuthProvider,\nlike lookup, blocked/deleted users
end

alt Successful case
"Client" ->> "Backend"  : access_token
"Backend" ->> "Backend" : Validate token
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" ->> "Backend" : Get data
"Backend" ->> "Client"  : Return data

else Token is expired
"Client" ->> "Backend"  : access_token
"Backend" ->> "Backend" : Validate token
"Backend" --x "Client"  : 401 Unauthorized

else User is blocked
"Client" ->> "Backend"  : access_token
"Backend" ->> "Backend" : Validate token
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" --x "Client"  : 401 Unauthorized

else User is deleted
"Client" ->> "Backend"  : access_token
"Backend" ->> "Backend" : Validate token
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" --x "Client"  : 404 Not found
end

deactivate "Client"
```

## Configuration { #cached_ldap-configuration }

Other settings are just the same as for `LDAPAuthProvider`

::: horizon.backend.settings.auth.cached_ldap.CachedLDAPAuthProviderSettings
  
::: horizon.backend.settings.auth.cached_ldap.LDAPCacheSettings

::: horizon.backend.settings.auth.cached_ldap.LDAPCachePasswordHashSettings
