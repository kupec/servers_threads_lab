FROM node:12-alpine

ARG variant

WORKDIR /app
COPY $variant.js app.js

ENTRYPOINT ["node", "app.js"]
