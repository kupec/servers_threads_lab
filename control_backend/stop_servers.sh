#!/bin/sh
set -e

cd /servers
./docker-compose.sh down --remove-orphans
