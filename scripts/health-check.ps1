$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Error "health check failed: $Message"
}

docker compose ps *> $null
if ($LASTEXITCODE -ne 0) { Fail "docker compose project is not available" }

# Bug fix: $env:POSTGRES_USER and $env:POSTGRES_DB may be unset if .env
# has not been sourced into the current shell.  Fall back to the same
# defaults used in docker-compose.yml and health-check.sh.
$pgUser = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "cyberlab" }
$pgDb   = if ($env:POSTGRES_DB)   { $env:POSTGRES_DB }   else { "cyberlab" }

docker compose exec -T database pg_isready -U $pgUser -d $pgDb *> $null
if ($LASTEXITCODE -ne 0) {
    docker compose exec -T database pg_isready -U cyberlab -d cyberlab *> $null
    if ($LASTEXITCODE -ne 0) { Fail "database is not ready" }
}

try {
    Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 5 | Out-Null
} catch {
    Fail "web app is not reachable on localhost:8080"
}

try {
    Invoke-RestMethod -Uri "http://localhost:8082/health" -TimeoutSec 5 | Out-Null
} catch {
    Fail "logging service is not reachable on localhost:8082"
}

$running = docker compose ps --services --filter status=running
$required = @("web", "logging", "database", "analyst-tools")
foreach ($service in $required) {
    if ($running -notcontains $service) { Fail "$service is not running" }
}

Write-Host "All required lab services are healthy."

