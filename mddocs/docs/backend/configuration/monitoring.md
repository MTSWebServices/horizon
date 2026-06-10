# Setup monitoring { #backend-configuration-monitoring }

Backend provides 2 endpoints with Prometheus compatible metrics:

- `GET /monitoring/metrics` - server metrics, like number of requests per path and response status, CPU and RAM usage, and so on.

## Example metrics

```
--8<--
mddocs/docs/_static/metrics.prom
--8<--
```

- `GET /monitoring/stats` - usage statistics, like number of users, namespaces, HWMs.

## Example stats

```
--8<--
mddocs/docs/_static/stats.prom
--8<--
```

These endpoints are enabled and configured using settings below:

::: horizon.backend.settings.server.monitoring.MonitoringSettings
