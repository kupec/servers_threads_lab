#!/usr/bin/env bash
set -e

if [[ ! -d hey ]]; then
    git clone https://github.com/rakyll/hey.git
fi;

docker build -t hey hey
docker build -t http_load .

docker run --rm \
    --env-file .env \
    -v "$PWD/reports:/reports" \
    -e "LOG_FILE=/reports/{}.log" \
    -it http_load
