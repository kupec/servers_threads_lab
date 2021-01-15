FROM alpine as builder
RUN apk update && apk add build-base

WORKDIR /app
COPY main.c .
RUN gcc -o app -static main.c

FROM nginx:alpine
RUN apk update && apk add fcgiwrap
RUN mkdir /fcgi && chmod 777 /fcgi
COPY default.conf /etc/nginx/conf.d
COPY --from=builder /app/app /fcgi/app
COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
