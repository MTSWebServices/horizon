# Exceptions { #client-exceptions }

These exception classes are used in client implementations.

## Base

::: horizon.commons.exceptions.base.ApplicationError
    options:
        show_root_heading: true
        members:
            - message
            - details

## Authorization

::: horizon.commons.exceptions.auth.AuthorizationError
    options:
        show_root_heading: true
        members:
            - message
            - details

## Permissions

::: horizon.commons.exceptions.permission.PermissionDeniedError
    options:
        show_root_heading: true
        members:
            - message
            - details
            - required_role
            - actual_role

::: horizon.commons.exceptions.bad_request.BadRequestError
    options:
        show_root_heading: true
        members:
            - reason

## Entity

::: horizon.commons.exceptions.entity.EntityNotFoundError
    options:
        show_root_heading: true
        members:
            - message
            - details
            - entity_type
            - field
            - value

::: horizon.commons.exceptions.entity.EntityAlreadyExistsError
    options:
        show_root_heading: true
        members:
            - message
            - details
            - entity_type
            - field
            - value

## Service

::: horizon.commons.exceptions.service.ServiceError
    options:
        show_root_heading: true
        members:
            - message
