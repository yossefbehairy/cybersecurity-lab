# Database

The lab uses the official PostgreSQL image. Schema and deterministic seed/reset logic live in `infrastructure/web/labapp/db.py`.

The database is attached only to `backend_net` and has no host-published port.

