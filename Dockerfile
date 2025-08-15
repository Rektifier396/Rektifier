FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Use a small entrypoint script that resolves the desired port through the
# Pydantic settings before handing control to Uvicorn. This avoids passing a
# placeholder like ``"${PORT}"`` directly to Uvicorn, which would otherwise
# cause it to crash on startup.
CMD ["./entrypoint.sh"]
