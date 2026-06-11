# Architecture { #backend-architecture }

```mermaid
stateDiagram-v2
[User] --> [RESTAPI]
[RESTAPI] --> [Database]
[RESTAPI] --> [LDAP]
```
