# Troubleshooting

## Docker daemon is not reachable

Start Docker Desktop and wait until it reports that the engine is running.

## Port already in use

Change the host-side ports in `docker-compose.yml`, then run:

```bash
docker compose up -d
```

## Health check fails

```bash
docker compose ps
docker compose logs --tail=100 web logging database
```

## Reset the lab

```bash
sh scripts/reset.sh
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/reset.ps1
```
