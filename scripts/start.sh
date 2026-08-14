#!/usr/bin/env sh
set -eu

docker compose up -d
sh scripts/health-check.sh

