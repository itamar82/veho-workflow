FROM python:3.11.7-slim

USER root

WORKDIR /opt/project

# Copy codebase to /app location
COPY . /opt/project

RUN exec python -m pip install -r requirements.txt ;
RUN exec python -m pip install -r requirements-test.txt ;

ENTRYPOINT [ "/opt/project/docker/entrypoint.sh" ]