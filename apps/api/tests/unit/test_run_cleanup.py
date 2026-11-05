from datetime import UTC, datetime, timedelta

import pytest

import app.services.cleanup.run_cleanup as run_cleanup_module
from app.core.config import settings
from app.services.cleanup.run_cleanup import run_cleanup
from app.types.account_summary import AccountSummary

NOW = datetime(2026, 11, 10, 12, 0, tzinfo=UTC)


@pytest.fixture
def deleted(monkeypatch):
    monkeypatch.setattr(settings, "setup_deadline_hours", 48)
    accounts = [
        AccountSummary("expired", NOW - timedelta(hours=100), False, []),
        AccountSummary("young", NOW - timedelta(hours=5), False, []),
        AccountSummary("kept", NOW - timedelta(hours=100), True, ["cvdone"]),
    ]
    removed: list[str] = []
    monkeypatch.setattr(run_cleanup_module, "iter_accounts", lambda: iter(accounts))
    monkeypatch.setattr(run_cleanup_module, "get_cv", lambda user_id: None)
    monkeypatch.setattr(run_cleanup_module, "delete_account", removed.append)
    return removed


def test_a_dry_run_reports_but_deletes_nothing(deleted):
    result = run_cleanup(NOW, dry_run=True)

    assert (result.checked, result.expired, result.deleted) == (3, 1, 0)
    assert deleted == []


def test_a_real_run_deletes_only_the_expired_accounts(deleted):
    result = run_cleanup(NOW, dry_run=False)

    assert (result.checked, result.expired, result.deleted) == (3, 1, 1)
    assert deleted == ["expired"]
