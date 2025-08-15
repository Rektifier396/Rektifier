FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Launch the application via ``python main.py`` so the ``Settings`` validator
# can sanitize any environment-provided ``PORT`` value before Uvicorn starts.
CMD ["python", "main.py"]
