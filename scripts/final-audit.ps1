$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Error "final audit failed: $Message"
}

docker compose config --quiet
if ($LASTEXITCODE -ne 0) { Fail "compose config is invalid" }

$heavy = Select-String -Path "docker-compose.yml","infrastructure/**/*.py" -Pattern "kibana|elastic|wazuh|5601" -CaseSensitive:$false
if ($heavy) { Fail "heavy logging stack reference found in v1 runtime files" }

$external = Select-String -Path "infrastructure/**/*.py","scripts/*","docker-compose.yml" -Pattern "https?://(?!(localhost|127\.0\.0\.1|logging|web|database))" -CaseSensitive:$false
if ($external) { Fail "external runtime target found" }

$running = docker compose ps --services --filter status=running
if ($running -notcontains "database") { Fail "database is not running" }

$dbPorts = docker inspect cyberlab-database --format "{{json .NetworkSettings.Ports}}"
if ($dbPorts -ne '{"5432/tcp":null}') { Fail "database appears to have a host-published port: $dbPorts" }

Write-Host "Final audit passed."
