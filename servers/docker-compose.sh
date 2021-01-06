#!/bin/sh

python3 make_docker_compose_json.py | docker-compose -f - "$@"
