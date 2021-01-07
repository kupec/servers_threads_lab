FROM alpine as builder
RUN apk update && apk add build-base

WORKDIR /app
COPY main.c .
RUN gcc -o app main.c

FROM alpine
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
