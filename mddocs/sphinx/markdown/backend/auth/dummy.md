<a id="backend-auth-dummy"></a>

# Dummy Auth provider

## Description

This auth provider allows to sign-in with any username and password, and and then issues an access token.

After successful auth, username is saved to backend database. It is then used for creating audit records for any object change, see `changed_by` field.

## Interaction schema

### Interaction schema

## Configuration
