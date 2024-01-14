FROM python:3.11.7-bullseye

USER root

RUN apt-get update
RUN apt-get -y install tini

COPY ./docker/files/start-service.sh /start-service.sh

WORKDIR /app

# Copy codebase to /app location
COPY . /app

RUN exec python -m pip install -r requirements.txt ;
RUN exec python -m pip install -r requirements-test.txt ;

ENV GUNICORN_WORKER_CLASS="uvicorn.workers.UvicornWorker"

ENTRYPOINT [ "docker/entrypoints/entrypoint.sh" ]