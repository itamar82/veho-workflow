#!/usr/bin/env bash
set -e

# If no arguments, drop into a bash shell.
# If arguments are passed and the first argument is "test", run the test suite,
# otherwise execute what was passed.
if [[ $# == 0 ]]; then
  /bin/bash
elif [[ $1 == "service" ]]; then
  shift
  uvicorn apps._devel:component --reload --port 8000 --host 0.0.0.0 --log-level debug --reload-dir apps
elif [[ $1 == "test" ]]; then
  shift
  pytest tests
elif [[ $1 == "lint" ]]; then
  shift
  isort .
  black .
  flake8 .
else
  exec "$@"
fi
