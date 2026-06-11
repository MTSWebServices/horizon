# Auth { #client-auth }

These classes are used for adding auth information to requests send from client.

::: horizon.client.auth.BaseAuth
    options:
        show_root_heading: true

::: horizon.client.auth.LoginPassword
    options:
        members:
            - login
            - password

::: horizon.client.auth.AccessToken
    options:
        members:
            - token
