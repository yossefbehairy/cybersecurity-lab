$ErrorActionPreference = "Stop"

docker compose exec -T web python -m labapp.db reset
try {
    Invoke-RestMethod -Method Post -Uri "http://localhost:8080/reset" | Out-Null
} catch {
    Write-Host "Web reset endpoint was not reachable; database reset command completed."
}
Write-Host "Lab state reset to deterministic baseline."

