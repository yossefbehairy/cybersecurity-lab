# Security Model

## Baseline

- Custom containers run as non-root users.
- Custom services drop all Linux capabilities.
- Custom services use `no-new-privileges:true`.
- Writable paths are limited with `read_only: true`, `tmpfs`, and named volumes.
- Credentials in `.env.example` are fake local-only values.

## Intentional Weaknesses

The Flask app contains controlled examples of SQL injection, stored XSS, IDOR, weak authorization, weak session posture, and insecure upload handling. They are included only to support local training scenarios.

## Out of Scope

- Public deployment
- Real offensive automation
- Real user data
- Production hardening of the intentionally vulnerable routes

