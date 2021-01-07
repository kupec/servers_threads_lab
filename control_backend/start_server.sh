#!/bin/sh
set -e

cd "$SERVERS_PATH/$1"
docker-compose -p servers up -d --build --remove-orphans
