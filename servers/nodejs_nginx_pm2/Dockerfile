FROM node:12-alpine
RUN npm install -g pm2

WORKDIR /app
COPY app.js .

ENTRYPOINT ["pm2", "start", "app.js", "-i", "max", "--no-daemon"]
