# Lab 01: Network Reconnaissance

Difficulty: Beginner  
Estimated Time: 30-45 min  
MITRE ATT&CK: T1595 - Active Scanning

## Learning Objectives

- Identify services inside the isolated lab network.
- Distinguish host-exposed services from internal-only services.
- Record evidence without scanning external systems.

## Prerequisites

- `make setup`, or on Windows PowerShell: `powershell -ExecutionPolicy Bypass -File scripts/setup.ps1`
- `docker compose exec analyst-tools sh`

## Scenario

You are a junior analyst asked to document the reachable services for Acme Supply's internal training network.

## Tasks

1. Resolve the `web` service from `analyst-tools`.
2. Enumerate open ports on the local `web` container only.
3. Visit the web health endpoint.
4. Capture evidence in your notes.

## Detection

The `/health` endpoint is intentionally excluded from security-event logging so Docker health checks do not create investigation noise. Record the service-resolution, HTTP, and local-only scan evidence from this exercise instead.

## Remediation

Explain why internal service discovery should be limited to approved scopes and why the database is not host-exposed.

## Verification

You can name the reachable training service, its port, and the network boundary that protects the database.
