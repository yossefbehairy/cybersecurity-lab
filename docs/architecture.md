# Architecture

The lab models a small internal ordering portal monitored by a lightweight SOC event collector.

## Components

- `web`: Flask application with controlled vulnerabilities and a minimal dashboard.
- `database`: PostgreSQL with fake users, products, orders, audit records, comments, and security events.
- `logging`: Flask API that stores structured security events in PostgreSQL.
- `analyst-tools`: constrained shell environment with only the tools required by the labs.

## Networks

- `lab_net`: internal network for analyst-to-web training traffic.
- `backend_net`: internal network for web, logging, and database traffic.
- `access_net`: host access bridge for localhost-bound web and logging ports.

The database has no host port. Only the web app and logging API bind to `127.0.0.1`.
