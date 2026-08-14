# Solution Guide

Expected pattern:

- repeated `auth.login.failure`
- eventual `auth.login.success`
- same username or source IP in a short time window

Fixes include rate limiting, account lockout thresholds, MFA, alerting, and user notification.

