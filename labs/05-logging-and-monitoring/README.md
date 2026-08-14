# Lab 05: Logging And Monitoring

Difficulty: Intermediate  
Estimated Time: 45-60 min  
MITRE ATT&CK: N/A - Defensive logging and monitoring exercise

## Learning Objectives

- Query structured security events.
- Filter events by type and severity.
- Explain what good SOC evidence looks like.

## Scenario

The SOC needs a lightweight event pipeline suitable for a laptop-based training lab.

## Tasks

1. Generate login, search, and upload events.
2. Query `/events?limit=20`.
3. Filter by severity or event type.
4. Identify source IP, endpoint, method, message, and raw context.

## Detection

Use `scripts/query-events.sh` on POSIX systems, `powershell -ExecutionPolicy Bypass -File scripts/query-events.ps1 -Limit 20` on Windows, or direct HTTP queries against localhost.

## Remediation

Recommend fields that should be mandatory in production logging and fields that should avoid sensitive data.

## Verification

You can reconstruct a simple timeline from structured events.
