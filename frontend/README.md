# Crypto Signal Dashboard

CoinMarketCap-style dashboard built with static HTML, Tailwind and vanilla
JavaScript. The interface talks to the FastAPI backend but falls back to
`mock/summary.json` when the API is unavailable.

## Local Development
Serve the static files in `frontend/public` with any web server. Example using
Python:

```bash
cd frontend/public
python -m http.server 8000
```

Visit [http://localhost:8000](http://localhost:8000) to view the dashboard.

## Deployment on Railway
Deploy as a static site or behind any CDN. No special build step is required.
