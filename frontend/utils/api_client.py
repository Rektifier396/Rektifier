"""HTTP client for interacting with the crypto signal backend."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed


class APIClient:
    """Simple wrapper around :mod:`httpx` with retry/backoff."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0) -> None:
        self.base_url = base_url or os.getenv("API_BASE_URL")
        if not self.base_url:
            raise ValueError("API_BASE_URL is not configured")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        response = self._client.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def health(self) -> Dict[str, Any]:
        """Return API health status."""
        return self._request("GET", "/health").json()

    def get_config(self) -> Dict[str, Any]:
        """Fetch current configuration from backend."""
        return self._request("GET", "/config").json()

    def update_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update configuration on backend."""
        return self._request("POST", "/config", json=data).json()

    def get_signal(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Fetch signal for a specific symbol and timeframe."""
        params = {"symbol": symbol, "timeframe": timeframe}
        return self._request("GET", "/signals", params=params).json()

    def get_signals_batch(self) -> List[Dict[str, Any]]:
        """Fetch batch signals for the configured watchlist."""
        return self._request("GET", "/signals/batch").json()

    def get_stats_daily(self, date: str) -> Dict[str, Any]:
        """Fetch daily statistics for the given date (YYYY-MM-DD)."""
        return self._request("GET", "/stats/daily", params={"date": date}).json()

    def backtest(self, symbol: str, timeframe: str, days: int) -> Dict[str, Any]:
        """Run backtest and return summary for the requested parameters."""
        params = {"symbol": symbol, "timeframe": timeframe, "days": days}
        return self._request("GET", "/backtest", params=params).json()


@lru_cache
def get_client() -> APIClient:
    """Return a cached :class:`APIClient` instance."""
    return APIClient()
