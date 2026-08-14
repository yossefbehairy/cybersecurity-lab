#!/usr/bin/env sh
set -eu

fail() {
  echo "final audit failed: $1" >&2
  exit 1
}

docker compose config --quiet || fail "compose config is invalid"

if grep -RInE "kibana|elastic|wazuh|5601" docker-compose.yml infrastructure; then
  fail "heavy logging stack reference found in v1 runtime files"
fi

external_refs="$(grep -RInE "https?://" infrastructure scripts docker-compose.yml || true)"
if [ -n "$external_refs" ] && echo "$external_refs" | grep -Ev "localhost|127\.0\.0\.1|logging|web|database" >/dev/null; then
  fail "external runtime target found"
fi

docker compose ps --services --filter status=running | grep -q '^database$' || fail "database is not running"

db_ports="$(docker inspect cyberlab-database --format '{{json .NetworkSettings.Ports}}')"
[ "$db_ports" = '{"5432/tcp":null}' ] || fail "database appears to have a host-published port: $db_ports"

echo "Final audit passed."
