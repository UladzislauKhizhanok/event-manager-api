FROM python:3.12.2-slim-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION  1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

COPY ./event_manager /event_manager

COPY docker-entrypoint.sh pyproject.toml poetry.lock /event_manager/

WORKDIR /event_manager

RUN chmod +x ./docker-entrypoint.sh

RUN poetry install --no-root --no-dev

ENTRYPOINT [ "./docker-entrypoint.sh" ]
