# Scenario

The `analyst-tools` container should be useful for learning but constrained enough to avoid becoming an unrestricted attack environment.

## Objective

Verify the analyst environment baseline and write down three hardening controls.

## Starting Conditions

Run:

```bash
make setup
docker compose exec analyst-tools sh
```

On Windows PowerShell, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
docker compose exec analyst-tools sh
```

## Tasks

1. Identify the current Linux user.
2. List the tools available for lab work.
3. Check whether common writable paths are limited.
4. Explain why this container has no published host ports.
