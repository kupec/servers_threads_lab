#!/usr/bin/env bash
source .env

if [[ ! -d hey ]]; then
    git clone https://github.com/rakyll/hey.git
fi;

function hey {
    docker-compose -f docker-compose.hey.yml run hey "$@"
}

for PORT in $(seq "$START_PORT" "$END_PORT"); do
    echo "======================"
    echo "|    PORT = $PORT    |"
    echo "======================"

    hey -n "$REQUEST_COUNT" -c "$CONCURRENCY" -t "$REQUEST_TIMEOUT" "http://$HOST:$PORT"

    echo; echo;
done;
