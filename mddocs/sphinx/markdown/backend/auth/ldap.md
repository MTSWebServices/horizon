<a id="backend-auth-ldap"></a>

# LDAP Auth provider

## Description

This auth provider checks for user credentials in LDAP, and and then issues an access token.

All requests to backend should be made with passing this access token. If token is expired, then new auth token should be issued.

After successful auth, username is saved to backend database. It is then used for creating audit records for any object change, see `changed_by` field.

#### WARNING
Until token is valid, no requests will be made to LDAP to check if user exists and not locked.
So do not set access token expiration time for too long (e.g. longer than a day).

## Strategies

#### NOTE
Basic LDAP terminology is explained here: [LDAP Overview](https://www.zytrax.com/books/ldap/ch2/)

There are 2 strategies to check for user in LDAP:

* Try to call `bind` request in LDAP with `DN` (`DistinguishedName`) and user password. `DN` is generated using `bind_dn_template`
* First try to *lookup* for user (`search` request) in LDAP to get user’s `DN` using some query, and then try to call `bind` using this `DN`. See `lookup settings`

By default, **lookup strategy is used**, as it can find user in a complex LDAP/ActiveDirectory environment. For example:

* you can search for user by `uid`, e.g. `(uid={login})` or `(sAMAccountName={login})`
* you can search for user by several attributes, e.g. `(|(uid={login})(mail={login}@domain.com))`
* you can filter for entries, like `(&(uid={login})(objectClass=person)`
* you can filter for users matching a specific group or some other condition, like `(&(uid={login})(memberOf=cn=MyPrettyGroup,ou=Groups,dc=mycompany,dc=com))`

After user is found in LDAP, its `uid_attribute` is used for audit records.

## Interaction schema

### No lookup

### With lookup

## Basic configuration

## Lookup-related configuration
