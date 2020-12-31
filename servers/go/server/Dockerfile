FROM golang:1.15 as builder

ENV USER=appuser
ENV UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

RUN apt-get update && apt-get install -y ca-certificates

WORKDIR /go/server
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o app main.go

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
USER appuser:appuser

COPY --from=builder /go/server/app /app
ENTRYPOINT ["/app"]
