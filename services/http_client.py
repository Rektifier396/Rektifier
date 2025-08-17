"""Shared HTTP client for outgoing requests."""
from __future__ import annotations

import httpx

_client: httpx.AsyncClient | None = None


def get_client() -> httpx.AsyncClient:
    """Return a singleton AsyncClient with sensible defaults."""
    global _client
    if _client is None:
        timeout = httpx.Timeout(10.0, connect=5.0)
        limits = httpx.Limits(max_connections=20, max_keepalive_connections=5)
        _client = httpx.AsyncClient(timeout=timeout, limits=limits)
    return _client


async def close_client() -> None:
    """Close the shared client if it was created."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
