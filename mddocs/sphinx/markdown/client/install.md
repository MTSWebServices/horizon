<a id="client-install"></a>

# Install client

## Requirements

* Python 3.7 or above
* Pydantic 1.x or 2.x

## Installation process

Install `data-horizon` package with following *extra* dependencies:

```console
$ pip install data-horizon[client-sync]
```

Available *extras* are:

* `client-sync` - [Sync client](sync.md#client-sync), based on [authlib](https://docs.authlib.org) and [requests](https://requests.readthedocs.io)
