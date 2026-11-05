from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.services.cleanup.find_expired_accounts import find_expired_accounts
from app.types.account_summary import AccountSummary

NOW = datetime(2026, 11, 10, 12, 0, tzinfo=UTC)


def account(user_id, hours_old, verified):
    return AccountSummary(user_id, NOW - timedelta(hours=hours_old), verified, [])


def test_returns_only_the_ids_of_expired_accounts(monkeypatch):
    monkeypatch.setattr(settings, "setup_deadline_hours", 48)
    accounts = [account("old", 100, False), account("young", 5, False), account("done", 100, True)]

    assert find_expired_accounts(accounts, NOW, lambda user_id: user_id == "done") == ["old"]


def test_returns_nothing_for_no_accounts():
    assert find_expired_accounts([], NOW, lambda user_id: False) == []
