import fastapi
from fastapi.testclient import TestClient

from main import app


def test_root_serves_ui() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Crypto Signal Dashboard" in response.content
