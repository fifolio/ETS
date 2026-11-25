import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.schemas.maintenance_result import MaintenanceResult

client = TestClient(app)
URL = "/internal/subscription-maintenance"


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    def fake(now, dry_run):
        recorded.append(dry_run)
        return MaintenanceResult(
            explore_renewals_due=1,
            expired_due=0,
            reminders_due=0,
            explore_renewed=0 if dry_run else 1,
            ended=0,
            reminded=0,
            failed=0,
            dry_run=dry_run,
        )

    monkeypatch.setattr("app.routers.internal.run_subscription_maintenance", fake)
    return recorded


def test_a_wrong_token_is_rejected(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    assert client.post(URL, headers={"X-Cleanup-Token": "wrong"}).status_code == 401
    assert calls == []


def test_the_default_is_a_dry_run(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    response = client.post(URL, headers={"X-Cleanup-Token": "secret"})

    assert response.status_code == 200 and response.json()["dry_run"] is True
    assert calls == [True]


def test_dry_run_false_really_runs_it(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    response = client.post(f"{URL}?dry_run=false", headers={"X-Cleanup-Token": "secret"})

    assert response.json()["explore_renewed"] == 1 and calls == [False]
