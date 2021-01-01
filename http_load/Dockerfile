FROM python:3.8-alpine
RUN apk update && apk add bash fzf
COPY --from=hey /hey /bin/hey
COPY .env hey.sh generate_http_load.py /
ENTRYPOINT ["python", "/generate_http_load.py"]
