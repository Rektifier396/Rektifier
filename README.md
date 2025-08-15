# Crypto Signal Bot

A simple crypto signal and backtesting bot using Binance public API, CoinGecko and Alternative.me. Built with FastAPI and designed for deployment on Railway.

## Features
- EMA/RSI based long/short signals with ATR risk management
- Background scheduler updates market data every minute
- REST API exposing signals, statistics and backtesting
- Basic vectorized backtester
- No API keys required

## Endpoints
- `GET /health` – service check
- `GET /signals` – signal for symbol/timeframe
- `GET /signals/batch` – all signals
- `GET /stats/daily` – daily market statistics
- `GET /backtest` – run quick backtest

## Development
```bash
pip install -r requirements.txt
# Start through the entrypoint script so environment-driven settings like
# ``PORT`` are validated before launching Uvicorn
./entrypoint.sh
```

## Tests
```bash
pytest
```

## Deployment on Railway
1. Create a new project and attach this repository.
2. Use the provided `Dockerfile` or `Procfile` (Docker build by default).
3. Ensure Python buildpacks install dependencies.
4. The service launches via `entrypoint.sh`, which validates the `$PORT`
   value before handing it to Uvicorn.

Environment variables can override defaults defined in `config.py` (e.g., `WATCHLIST`, `TIMEFRAMES`).
