from fastapi.testclient import TestClient

from app.main import app
from app.schemas.site_totals import SiteTotals

client = TestClient(app)

TOTALS = SiteTotals(
    total_users=12,
    total_scans=340,
    total_minutes_saved=1500.0,
    total_hours_saved=25.0,
    total_cash_saved_usd=1250.5,
)


def test_the_totals_are_public(monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_site_totals", lambda: TOTALS)

    response = client.get("/stats/totals")

    assert response.status_code == 200
    assert response.json() == TOTALS.model_dump()


def test_the_totals_can_be_cached(monkeypatch):
    monkeypatch.setattr("app.routers.stats.get_site_totals", lambda: TOTALS)

    assert "max-age=86400" in client.get("/stats/totals").headers["cache-control"]
