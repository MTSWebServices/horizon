# Manage Admins { #manage-admins-script }

```console
$ python -m horizon.backend.scripts.manage_admins [-h] {add,remove,list} ...

Manage admin users.

positional arguments:
  {add,remove,list}
    add              Add admin privileges to users
    remove           Remove admin privileges from users
    list             List all admins
```

## add

```console
$ python -m horizon.backend.scripts.manage_admins add [-h] [usernames ...]

positional arguments:
  usernames   Usernames to add as admins, defaults to settings.admin_users
```

When no usernames are passed, the command uses the `admin_users` list from application settings.

## remove

```console
$ python -m horizon.backend.scripts.manage_admins remove [-h] usernames [usernames ...]

positional arguments:
  usernames   Usernames to remove from admins
```

## list

```console
$ python -m horizon.backend.scripts.manage_admins list [-h]
```
