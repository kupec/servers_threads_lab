#!/bin/sh

pm2 start app.js -i max;
nginx -g "daemon off;"
