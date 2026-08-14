param(
    [int]$Limit = 20
)

$events = Invoke-RestMethod -Uri "http://localhost:8082/events?limit=$Limit"
$events | ConvertTo-Json -Depth 8

