#!/bin/sh
set -e

cd /servers
./docker-compose.sh up -d --remove-orphans "$@"
