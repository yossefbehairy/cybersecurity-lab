# Scenario

The SOC sees suspicious product searches, failed logins, and access to admin audit data.

## Objective

Correlate multiple event types and write a concise incident report.

## Tasks

1. Generate a suspicious search event.
2. Generate failed login events, then log in successfully with `alice` / `Password123!`.
3. Trigger weak audit access.
4. Query recent events.
5. Identify initial signal, affected endpoint, likely impact, containment, recovery, and verification.
