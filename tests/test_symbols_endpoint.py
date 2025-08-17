from fastapi.testclient import TestClient

from main import app
from config import settings


def test_symbols_endpoint_returns_watchlist_and_cors() -> None:
    client = TestClient(app)
    response = client.get("/symbols", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert response.json() == settings.watchlist
    assert response.headers.get("access-control-allow-origin") == "*"
