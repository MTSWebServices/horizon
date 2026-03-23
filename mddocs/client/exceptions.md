# Exceptions { #client-exceptions }

These exception classes are used in client implementations.

## Base

::: horizon.commons.exceptions.base.ApplicationError
    options:
        members:
            - message
            - details

## Authorization

::: horizon.commons.exceptions.auth.ApplicationError
    options:
        members:
            - message
            - details

## Permissions

::: horizon.commons.exceptions.permission.PermissionDeniedError
    options:
        members:
            - message
            - details
            - required_role
            - actual_role

::: horizon.commons.exceptions.bad_request.BadRequestError
    options:
        members:
            - reason

## Entity

### *class* horizon.commons.exceptions.entity.EntityNotFoundError(entity_type: str, field: str, value: Any)

::: horizon.commons.exceptions.entity.EntityNotFoundError
    options:
        members:
            - message
            - details
            - entity_type
            - field
            - value

::: horizon.commons.exceptions.entity.EntityAlreadyExistsError
    options:
        members:
            - message
            - details
            - entity_type
            - field
            - value

## Service

::: horizon.commons.exceptions.service.ServiceError
    options:
        members:
            - message
