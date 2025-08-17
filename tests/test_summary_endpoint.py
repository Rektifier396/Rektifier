from fastapi.testclient import TestClient

from main import app


def test_summary_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/summary", params={"interval": "15m"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["interval"] == "15m"
    assert isinstance(data.get("data"), list)
    if data["data"]:
        first = data["data"][0]
        assert {"symbol", "price", "rsi"}.issubset(first.keys())
