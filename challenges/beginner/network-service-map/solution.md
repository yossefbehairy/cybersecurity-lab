# Solution Guide

Expected finding: the analyst container can reach `web:8080` inside `lab_net`. It should not reach the database directly because `database` is only on `backend_net`.

Good evidence includes:

- resolved service name
- HTTP health response
- local-only scan output
- note that Docker networks are internal

