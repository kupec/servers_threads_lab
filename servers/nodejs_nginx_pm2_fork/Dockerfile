FROM node:12-alpine
RUN npm install -g pm2

WORKDIR /app
COPY app.js .
COPY app.config.js .

ENTRYPOINT ["pm2", "start", "app.config.js", "--no-daemon"]
