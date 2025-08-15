# Crypto Signal Dashboard

Streamlit dashboard that consumes the FastAPI crypto signal backend.

## Local Development
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `API_BASE_URL` to your backend URL.
4. Run the app:
   ```bash
   streamlit run frontend/app.py
   ```

## Deployment on Railway
1. Push this repository to GitHub.
2. Create a new Railway project and connect the repo.
3. Set the `API_BASE_URL` environment variable pointing to your backend service.
4. Railway uses the provided `Procfile` to start the Streamlit server.
