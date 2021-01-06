#!/bin/sh
set -e

cd /servers
python make_docker_compose_json.py
