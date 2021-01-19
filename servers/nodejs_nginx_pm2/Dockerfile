FROM nginx:alpine
RUN apk update && apk add nodejs npm 
RUN npm install -g pm2

WORKDIR /app
COPY app.js .
COPY default.conf /etc/nginx/conf.d
COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
