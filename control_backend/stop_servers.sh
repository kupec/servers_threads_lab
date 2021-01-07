#!/bin/sh
set -e

cd "$SERVERS_PATH"
docker-compose -p servers down --remove-orphans
