#!/usr/bin/env sh
set -eu

if ! command -v docker >/dev/null 2>&1; then
  echo "docker was not found. Install Docker Desktop and start it before running setup." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon is not reachable. Start Docker Desktop, then retry." >&2
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example with local-only training values."
fi

docker compose build
docker compose up -d
sh scripts/health-check.sh

echo
echo "Cybersecurity Training Lab is ready."
echo "Web app:      http://localhost:8080"
echo "Logging API:  http://localhost:8082/events?limit=20"
echo "Analyst shell: docker compose exec analyst-tools sh"

