FROM python:3.8.2-slim as base

FROM base as builder

RUN apt update && apt install -y \
    gcc \
    git \
    libpq-dev \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip install pip==20.1.1

WORKDIR /install

FROM builder as dev
WORKDIR /opt/fecundityllc
COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt
COPY . ./

FROM builder as prod_builder
COPY requirements/prod.txt /prod.txt
RUN pip install --prefix=/install --no-warn-script-location -r /prod.txt

FROM base as prod
RUN apt update && apt install -y postgresql-client binutils libproj-dev gdal-bin
COPY --from=prod_builder /install /usr/local
WORKDIR /opt/fecundityllc
COPY . ./
EXPOSE 8000
