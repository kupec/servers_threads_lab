FROM python:3.8-alpine
RUN apk update && apk add build-base libressl-dev musl-dev libffi-dev
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry add gunicorn && poetry install

COPY . .

CMD ["poetry", "run", "gunicorn", "-w", "50", "-b", "0.0.0.0:8000", "backend.wsgi"]
