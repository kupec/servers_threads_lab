#!/bin/sh

WORKERS=250

for i in $(seq 1 $WORKERS); do
    su -s /bin/sh nginx -c "fcgiwrap -s unix:/fcgi/fcgi_$i.sock" &
done;
nginx -g "daemon off;"
