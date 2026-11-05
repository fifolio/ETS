import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.schemas.cleanup_result import CleanupResult

client = TestClient(app)
URL = "/internal/cleanup-unactivated-accounts"


@pytest.fixture
def calls(monkeypatch):
    recorded = []

    def fake_run_cleanup(now, dry_run):
        recorded.append(dry_run)
        return CleanupResult(checked=3, expired=1, deleted=0 if dry_run else 1, dry_run=dry_run)

    monkeypatch.setattr("app.routers.internal.run_cleanup", fake_run_cleanup)
    return recorded


def test_the_cleanup_is_disabled_without_a_token_setting(monkeypatch):
    monkeypatch.setattr(settings, "cleanup_token", "")
    assert client.post(URL, headers={"X-Cleanup-Token": "anything"}).status_code == 503


def test_a_wrong_token_is_rejected(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    assert client.post(URL, headers={"X-Cleanup-Token": "wrong"}).status_code == 401
    assert client.post(URL).status_code == 401
    assert calls == []


def test_the_default_is_a_dry_run(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    response = client.post(URL, headers={"X-Cleanup-Token": "secret"})

    assert response.status_code == 200
    assert response.json()["dry_run"] is False
    assert calls == [False]


def test_dry_run_false_really_runs_it(monkeypatch, calls):
    monkeypatch.setattr(settings, "cleanup_token", "secret")

    response = client.post(f"{URL}?dry_run=false", headers={"X-Cleanup-Token": "secret"})

    assert response.json()["deleted"] == 1
    assert calls == [False]
