#!/bin/sh

su -s /bin/sh nginx -c 'fcgiwrap -s unix:/fcgi/fcgi.sock' &
nginx -g "daemon off;"
