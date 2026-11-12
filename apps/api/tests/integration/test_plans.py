from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


def test_the_plans_are_public(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "none")

    response = client.get("/plans")

    assert response.status_code == 200
    body = response.json()
    assert [plan["id"] for plan in body["plans"]] == ["explore", "nextmove", "urgent"]
    assert body["payments_enabled"] is False


def test_the_plans_can_be_cached():
    assert "max-age=300" in client.get("/plans").headers["cache-control"]
