# Network Model

## Allowed Communication

| Source | Destination | Purpose |
| --- | --- | --- |
| Host | `localhost:8080` | Browser access to vulnerable app |
| Host | `localhost:8082` | Local log review |
| `analyst-tools` | `web:8080` | Lab-only reconnaissance and HTTP analysis |
| `web` | `logging:8082` | Security event emission |
| `web` | `database:5432` | Application data |
| `logging` | `database:5432` | Event storage |

## Boundaries

- `analyst-tools` has no published ports.
- `database` is not exposed to the host.
- `lab_net` and `backend_net` are `internal: true`.
- `access_net` exists only for localhost-bound browser/API access to web and logging.
