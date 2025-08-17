FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run the application through the main module so the settings validator can
# sanitize dynamic environment values like ``PORT`` before passing them to
# Uvicorn.
# Use an entrypoint so platforms that override the container command still
# execute the main module. ``main.py`` sanitizes environment variables like
# ``PORT`` before handing them off to Uvicorn, preventing errors such as
# ``Invalid value for '--port': ${PORT} is not a valid integer``.
ENTRYPOINT ["python", "main.py"]
