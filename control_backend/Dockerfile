FROM python:3.8-alpine
rUN apk update && apk add build-base libressl-dev musl-dev libffi-dev docker-cli rust cargo
RUN pip install poetry docker-compose

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY server.py /
COPY start_server.sh /
COPY stop_servers.sh /
ENTRYPOINT ["poetry", "run", "python", "/server.py"]
