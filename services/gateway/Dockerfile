FROM python:3.9.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /gateway && apt-get update && apt-get install -y gettext
WORKDIR /gateway

COPY ./pyproject.toml /gateway/
COPY ./poetry.lock /gateway/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./ /gateway
