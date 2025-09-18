<a id="client-exceptions"></a>

# Exceptions

These exception classes are used in client implementations.

## Base

### *class* horizon.commons.exceptions.base.ApplicationError

Base class for all exceptions raised by Horizon.

* **Attributes:**
  [`details`](#horizon.commons.exceptions.base.ApplicationError.details)
  : Details related to specific error

  [`message`](#horizon.commons.exceptions.base.ApplicationError.message)
  : Message string

<!-- !! processed by numpydoc !! -->

#### *abstract property* details *: Any*

Details related to specific error

<!-- !! processed by numpydoc !! -->

#### *abstract property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->

## Authorization

### *class* horizon.commons.exceptions.auth.AuthorizationError(message: str, details: Any = None)

Authorization request is failed.

* **Attributes:**
  [`details`](#horizon.commons.exceptions.auth.AuthorizationError.details)
  : Details related to specific error

  [`message`](#horizon.commons.exceptions.auth.AuthorizationError.message)
  : Message string

### Examples

```pycon
>>> from horizon.commons.exceptions import AuthorizationError
>>> raise AuthorizationError("User 'test' is disabled")
Traceback (most recent call last):
horizon.commons.exceptions.auth.AuthorizationError: User 'test' is disabled
```

<!-- !! processed by numpydoc !! -->

#### *property* details *: Any*

Details related to specific error

<!-- !! processed by numpydoc !! -->

#### *property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->

## Permissions

### *class* horizon.commons.exceptions.permission.PermissionDeniedError(required_role: str, actual_role: str)

Permission denied for performing the requested action.

* **Attributes:**
  [`details`](#horizon.commons.exceptions.permission.PermissionDeniedError.details)
  : Details related to specific error

  [`message`](#horizon.commons.exceptions.permission.PermissionDeniedError.message)
  : Message string

### Examples

```pycon
>>> from horizon.commons.exceptions import PermissionDeniedError
>>> raise PermissionDeniedError(required_role="DEVELOPER", actual_role="GUEST")
Traceback (most recent call last):
horizon.commons.exceptions.PermissionDeniedError: Permission denied. User has role GUEST but action requires at least DEVELOPER.
```

<!-- !! processed by numpydoc !! -->

#### required_role *: str*

Required role to perform action

<!-- !! processed by numpydoc !! -->

#### actual_role *: str*

Actual user role

<!-- !! processed by numpydoc !! -->

#### *property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->

#### *property* details *: dict[str, Any]*

Details related to specific error

<!-- !! processed by numpydoc !! -->

### *class* horizon.commons.exceptions.bad_request.BadRequestError(reason: str)

Bad request error.

This exception should be raised when a request cannot be processed due to
client-side errors (e.g., invalid data, duplicate entries).

### Examples

```pycon
>>> from horizon.commons.exceptions import BadRequestError
>>> raise BadRequestError("Duplicate username detected. Each username must appear only once.")
Traceback (most recent call last):
horizon.commons.exceptions.BadRequestError: Duplicate username detected. Each username must appear only once.
```

<!-- !! processed by numpydoc !! -->

#### reason *: str*

Bad request reason message

<!-- !! processed by numpydoc !! -->

## Entity

### *class* horizon.commons.exceptions.entity.EntityNotFoundError(entity_type: str, field: str, value: Any)

Entity not found.

* **Attributes:**
  [`details`](#horizon.commons.exceptions.entity.EntityNotFoundError.details)
  : Details related to specific error

  [`message`](#horizon.commons.exceptions.entity.EntityNotFoundError.message)
  : Message string

### Examples

```pycon
>>> from horizon.commons.exceptions import EntityNotFoundError
>>> raise EntityNotFoundError("User", "username", "test")
Traceback (most recent call last):
horizon.commons.exceptions.entity.EntityNotFoundError: User with username='test' not found
```

<!-- !! processed by numpydoc !! -->

#### entity_type *: str*

Entity type

<!-- !! processed by numpydoc !! -->

#### field *: str*

Entity identifier field

<!-- !! processed by numpydoc !! -->

#### value *: Any*

Entity identifier value

<!-- !! processed by numpydoc !! -->

#### *property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->

#### *property* details *: dict[str, Any]*

Details related to specific error

<!-- !! processed by numpydoc !! -->

### *class* horizon.commons.exceptions.entity.EntityAlreadyExistsError(entity_type: str, field: str, value: Any)

Entity with same identifier already exists.

* **Attributes:**
  [`details`](#horizon.commons.exceptions.entity.EntityAlreadyExistsError.details)
  : Details related to specific error

  [`message`](#horizon.commons.exceptions.entity.EntityAlreadyExistsError.message)
  : Message string

### Examples

```pycon
>>> from horizon.commons.exceptions import EntityNotFoundError
>>> raise EntityAlreadyExistsError("User", "username", "test")
Traceback (most recent call last):
horizon.commons.exceptions.entity.EntityAlreadyExistsError: User with username='test' already exists
```

<!-- !! processed by numpydoc !! -->

#### entity_type *: str*

Entity type

<!-- !! processed by numpydoc !! -->

#### field *: str*

Entity identifier field

<!-- !! processed by numpydoc !! -->

#### value *: Any*

Entity identifier value

<!-- !! processed by numpydoc !! -->

#### *property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->

#### *property* details *: dict[str, Any]*

Details related to specific error

<!-- !! processed by numpydoc !! -->

## Service

### *class* horizon.commons.exceptions.service.ServiceError(message: str)

Service used by application have not responded properly.

* **Attributes:**
  [`message`](#horizon.commons.exceptions.service.ServiceError.message)
  : Message string

### Examples

```pycon
>>> from horizon.commons.exceptions import ServiceError
>>> raise ServiceError("Some server response is invalid")
Traceback (most recent call last):
horizon.commons.exceptions.service.ServiceError: Some server response is invalid
```

<!-- !! processed by numpydoc !! -->

#### *property* message *: str*

Message string

<!-- !! processed by numpydoc !! -->
