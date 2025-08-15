#!/usr/bin/env bash
set -e

# Determine a safe port using the application's settings module.
PORT_SANITIZED=$(python - <<'PY'
from config import settings
print(settings.port)
PY
)

exec uvicorn main:app --host 0.0.0.0 --port "${PORT_SANITIZED}"
