# Solution Guide

The route trusts `?role=admin`, which is user-controlled and not tied to authenticated server-side authorization.

Evidence:

- `403` without the parameter
- audit records with `?role=admin`
- `authz.role-bypass` event

Fix: require authentication and check the user's server-side role from the database or signed session.

