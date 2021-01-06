#!/usr/bin/env bash
set -e

cd ../servers
./docker-compose.sh build
cd -

docker-compose build backend
docker-compose run --rm -p 3000:3000 backend
