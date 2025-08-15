FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run the application through the main module so the settings validator can
# sanitize dynamic environment values like ``PORT`` before passing them to
# Uvicorn.
CMD ["python", "main.py"]
