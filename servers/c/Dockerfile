FROM alpine as builder

ARG variant

RUN apk update && apk add build-base

WORKDIR /app
COPY $variant.c .
RUN gcc -o app $variant.c

FROM alpine
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
