#!/usr/bin/env bash
set -euo pipefail

if [[ $# == 0 ]]; then
    gunicorn \
    "apps.api.component:create_app()" \
    -b ":${GUNICORN_PORT:-5000}" \
    -w "${GUNICORN_WORKERS:-2}" \
    -k "${GUNICORN_WORKER_CLASS:-gevent}" \
    --log-level="${GUNICORN_LOG_LEVEL:-INFO}" \
    --worker-connections="${GUNICORN_WORKER_CONNECTIONS:-5000}" \
    --max-requests="${GUNICORN_MAX_REQUESTS:-5000}" \
    --max-requests-jitter="${GUNICORN_MAX_REQUESTS_JITTER:-500}"

else  
  echo "$@"
fi
