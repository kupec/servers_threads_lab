FROM alpine as builder
RUN apk update && apk add build-base

WORKDIR /app
COPY main.c .
RUN gcc -o app -static main.c

FROM httpd

COPY --from=builder /app/app ./htdocs/app.cgi
COPY config .
RUN cat config >> conf/httpd.conf
