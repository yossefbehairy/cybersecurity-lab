#!/usr/bin/env sh
set -eu

docker compose exec -T web python -m labapp.db reset
curl -fsS -X POST http://localhost:8080/reset >/dev/null || true
echo "Lab state reset to deterministic baseline."

