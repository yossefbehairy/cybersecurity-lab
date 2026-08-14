#!/usr/bin/env sh
set -eu

fail() {
  echo "health check failed: $1" >&2
  exit 1
}

docker compose ps >/dev/null || fail "docker compose project is not available"
docker compose exec -T database pg_isready -U "${POSTGRES_USER:-cyberlab}" -d "${POSTGRES_DB:-cyberlab}" >/dev/null || fail "database is not ready"
curl -fsS http://localhost:8080/health >/dev/null || fail "web app is not reachable on localhost:8080"
curl -fsS http://localhost:8082/health >/dev/null || fail "logging service is not reachable on localhost:8082"

web_count="$(docker compose ps --services --filter status=running | grep -E '^(web|logging|database|analyst-tools)$' | wc -l | tr -d ' ')"
[ "$web_count" = "4" ] || fail "expected 4 running services, found $web_count"

echo "All required lab services are healthy."

