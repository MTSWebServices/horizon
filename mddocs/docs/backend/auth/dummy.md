# Dummy Auth provider { #backend-auth-dummy }

## Description { #dummy-description }

This auth provider allows to sign-in with any username and password, and and then issues an access token.

After successful auth, username is saved to backend database. It is then used for creating audit records for any object change, see `changed_by` field.

## Interaction schema { #dummy-interaction-schema }

```mermaid
sequenceDiagram
participant "Client"
participant "Backend"

activate "Client"
alt Successful case
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Password is completely ignored
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" ->> "Backend" : Create user if not exist
"Backend" ->> "Client"  : Generate and return access_token

else User is blocked
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Password is completely ignored
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" --x "Client"  : 401 Unauthorized

else User is deleted
"Client" ->> "Backend"  : login + password
"Backend" ->> "Backend" : Password is completely ignored
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" --x "Client"  : 404 Not found
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

else
"Client" ->> "Backend"  : access_token
"Backend" ->> "Backend" : Validate token
"Backend" ->> "Backend" : Check user in internal backend database
"Backend" --x "Client"  : 404 Not found
end

deactivate "Client"
```

## Configuration { #dummy-configuration }

::: horizon.backend.settings.auth.dummy.DummyAuthProviderSettings

::: horizon.backend.settings.auth.jwt.JWTSettings
