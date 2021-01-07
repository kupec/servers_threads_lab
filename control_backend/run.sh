#!/usr/bin/env bash
set -e

docker-compose build backend
docker-compose run --rm -p 3000:3000 backend
