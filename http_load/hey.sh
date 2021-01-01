#!/usr/bin/env bash
set -e

source .env
hey -n "$REQUEST_COUNT" -c "$CONCURRENCY" -t "$REQUEST_TIMEOUT" "http://$HOST:3001"
