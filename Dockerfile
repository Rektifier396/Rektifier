FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Launch via ``entrypoint.sh`` which computes a safe port before invoking Uvicorn.
CMD ["./entrypoint.sh"]
