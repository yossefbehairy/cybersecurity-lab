#!/usr/bin/env sh
set -eu

limit="${1:-20}"
curl -fsS "http://localhost:8082/events?limit=${limit}" | jq .

