#!/usr/bin/env bash
# Launch the FastAPI application with a validated port value.
# Some hosting environments populate PORT with a placeholder like "${PORT}",
# which causes Uvicorn to fail.  Use the Pydantic settings to coerce any such
# value to a usable integer before invoking Uvicorn.
set -e
PORT_COERCED=$(python - <<'PY'
from config import settings
print(settings.port)
PY
)
exec uvicorn main:app --host 0.0.0.0 --port "$PORT_COERCED"
