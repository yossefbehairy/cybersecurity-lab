# Solution Guide

The expected user is `analyst`, not `root`. The container includes a limited toolset for lab-only HTTP, DNS, port, JSON, and PostgreSQL client work.

Evidence should mention:

- `read_only: true`
- `cap_drop: ALL`
- `security_opt: no-new-privileges:true`
- no `ports:` mapping for `analyst-tools`

Remediation concept: analyst environments should be scoped to approved targets and minimal required tools.

