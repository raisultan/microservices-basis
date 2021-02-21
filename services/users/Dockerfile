FROM python:3.9.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /users && apt-get update && apt-get install -y gettext
WORKDIR /users

COPY ./pyproject.toml /users/
COPY ./poetry.lock /users/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./ /users
