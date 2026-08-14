# Installation

## Prerequisites

- Docker Desktop running
- Docker Compose plugin
- Optional: `make`

## Setup

```bash
cp .env.example .env
sh scripts/setup.sh
```

PowerShell:

```powershell
Copy-Item .env.example .env
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
```

## Verify

```bash
sh scripts/health-check.sh
docker compose ps
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/health-check.ps1
docker compose ps
```

Expected local URLs:

- `http://localhost:8080`
- `http://localhost:8082/events?limit=20`
