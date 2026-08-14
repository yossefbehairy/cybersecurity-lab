$ErrorActionPreference = "Stop"

docker compose up -d
powershell -ExecutionPolicy Bypass -File scripts/health-check.ps1

