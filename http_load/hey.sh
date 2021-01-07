#!/usr/bin/env bash
set -e

source .env
hey -n "$REQUEST_COUNT" -c "$CONCURRENCY" -t "$REQUEST_TIMEOUT" -z "${TOTAL_TIMEOUT}s" "http://$HOST:3001"
