#/bin/sh
set -e

WORKERS=250

{
    echo "upstream cgi_back {";
    for i in $(seq 1 $WORKERS); do
        echo "    server unix:/fcgi/fcgi_$i.sock;";
    done;
    echo "}";
} >> /etc/nginx/conf.d/default.conf

