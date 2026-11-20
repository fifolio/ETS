from fastapi.testclient import TestClient

from app.main import app
from app.schemas.currency_out import CurrencyOut

client = TestClient(app)
USD = CurrencyOut(code="usd", name="US Dollar", symbol="$", rate_from_usd=1.0)


def test_currencies_are_public_and_cached(monkeypatch):
    monkeypatch.setattr("app.routers.currencies.list_currencies", lambda: [USD])
    response = client.get("/currencies")
    assert response.status_code == 200
    assert response.json()[0]["symbol"] == "$"
    assert "max-age=300" in response.headers["cache-control"]
