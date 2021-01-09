FROM golang:1.15 as builder
WORKDIR /go/server
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o app main.go

FROM scratch
COPY --from=builder /go/server/app /app
ENTRYPOINT ["/app"]
