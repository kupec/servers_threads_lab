#!/usr/bin/env bash
source .env

if [[ ! -d hey ]]; then
    git clone https://github.com/rakyll/hey.git
fi;

docker-compose -f docker-compose.hey.yml run hey -n "$REQUEST_COUNT" -c "$CONCURRENCY" "http://$HOST:3001"
