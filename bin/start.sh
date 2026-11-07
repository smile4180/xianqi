#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -x .venv/bin/python ]; then
  echo 'Virtual environment missing. Follow README setup instructions first.' >&2
  exit 1
fi
exec .venv/bin/python app_server.py
