$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "docker was not found. Install Docker Desktop and start it before running setup."
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker daemon is not reachable. Start Docker Desktop, then retry."
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example with local-only training values."
}

docker compose build
docker compose up -d
powershell -ExecutionPolicy Bypass -File scripts/health-check.ps1

Write-Host ""
Write-Host "Cybersecurity Training Lab is ready."
Write-Host "Web app:      http://localhost:8080"
Write-Host "Logging API:  http://localhost:8082/events?limit=20"
Write-Host "Analyst shell: docker compose exec analyst-tools sh"

