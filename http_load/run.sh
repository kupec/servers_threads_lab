#!/usr/bin/env bash
set -e

if [[ ! -d hey ]]; then
    git clone https://github.com/rakyll/hey.git
fi;

docker build -t hey hey
docker-compose build http_load

docker-compose run http_load
