from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

import app.services.cleanup.run_cleanup as module
from app.core.config import settings
from app.types.account_summary import AccountSummary

NOW = datetime(2026, 11, 10, 12, 0, tzinfo=UTC)


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setattr(settings, "setup_deadline_hours", 48)
    accounts = [
        AccountSummary("expired", NOW - timedelta(hours=100), False, []),
        AccountSummary("young", NOW - timedelta(hours=5), False, []),
        AccountSummary("kept", NOW - timedelta(hours=100), True, ["cvdone"]),
    ]
    calls = SimpleNamespace(accounts=[], data=[])
    monkeypatch.setattr(module, "iter_accounts", lambda: iter(accounts))
    monkeypatch.setattr(module, "get_cv", lambda user_id: None)
    monkeypatch.setattr(
        module, "find_data_owner_ids", lambda: {"expired", "young", "kept", "ghost"}
    )
    monkeypatch.setattr(module, "delete_user_account", calls.accounts.append)
    monkeypatch.setattr(module, "delete_user_data", calls.data.append)
    return SimpleNamespace(calls=calls, monkeypatch=monkeypatch)


def test_a_dry_run_reports_everything_but_deletes_nothing(env):
    result = module.run_cleanup(NOW, dry_run=True)

    assert (result.checked, result.expired, result.deleted) == (3, 1, 0)
    assert (result.orphaned, result.orphans_cleaned) == (1, 0)
    assert env.calls.accounts == [] and env.calls.data == []


def test_a_real_run_deletes_expired_accounts_and_the_data_of_deleted_users(env):
    result = module.run_cleanup(NOW, dry_run=False)

    assert (result.deleted, result.orphans_cleaned, result.failed) == (1, 1, 0)
    assert env.calls.accounts == ["expired"]
    assert env.calls.data == ["ghost"]


def test_one_failure_is_counted_and_the_rest_still_runs(env):
    def fail(user_id):
        raise RuntimeError("storage down")

    env.monkeypatch.setattr(module, "delete_user_data", fail)

    result = module.run_cleanup(NOW, dry_run=False)

    assert (result.deleted, result.orphans_cleaned, result.failed) == (1, 0, 1)


def test_nothing_is_swept_when_no_accounts_were_found(env):
    env.monkeypatch.setattr(module, "iter_accounts", lambda: iter([]))

    result = module.run_cleanup(NOW, dry_run=False)

    assert (result.checked, result.orphaned) == (0, 0)
    assert env.calls.data == []
