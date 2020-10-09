FROM python:3.8.2-slim as dev
RUN apt update && apt install -y \
    gcc \
    git \
    libpq-dev \
    postgresql-client

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip install pip==20.2.3

WORKDIR /opt/fecundityllc

COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt

COPY . ./
