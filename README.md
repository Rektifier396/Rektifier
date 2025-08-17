# Crypto Signal Bot

A simple crypto signal and backtesting bot using Binance public API, CoinGecko and Alternative.me. Built with FastAPI and designed for deployment on Railway. The service now ships with a lightweight dashboard served from the root URL.

## Features
- EMA/RSI based long/short signals with ATR risk management
- Background scheduler updates market data every minute
- REST API exposing signals, statistics and backtesting
- Basic vectorized backtester
- No API keys required

## Endpoints
The FastAPI backend exposes several JSON endpoints:
- `GET /health` – service check
- `GET /symbols` – list supported symbols
- `GET /signals` – signal for symbol/timeframe
- `GET /signals/batch` – all signals
- `GET /stats/daily` – daily market statistics
- `GET /backtest` – run quick backtest

Opening the root path (`/`) in a browser will display a simple web UI that fetches data from the API.

## Development
```bash
pip install -r requirements.txt
# Run through the main module so environment-driven settings like ``PORT``
# are validated before launching Uvicorn
python main.py
```

## Tests
```bash
pytest
```

## Deployment on Railway
1. Create a new project and attach this repository.
2. Use the provided `Dockerfile` or `Procfile` (Docker build by default).
3. Ensure Python buildpacks install dependencies.
4. The service will listen on `$PORT` provided by Railway.

Environment variables can override defaults defined in `config.py` (e.g., `WATCHLIST`, `TIMEFRAMES`).
