#!/bin/sh
set -e

cd /servers
docker-compose up -d "$@"
