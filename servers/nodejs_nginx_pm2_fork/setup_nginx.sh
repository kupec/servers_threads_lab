#/bin/sh
set -e

CPU_COUNT=$(cat /proc/cpuinfo | grep processor | wc -l)
let "MAX_PORT = CPU_COUNT - 1 + 3000"

{
    echo "upstream back {";
    for PORT in $(seq 3000 $MAX_PORT); do
        echo "    server backend:$PORT;";
    done;
    echo "}";
} >> /etc/nginx/conf.d/default.conf
