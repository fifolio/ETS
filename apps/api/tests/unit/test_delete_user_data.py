import pytest

import app.services.account.delete_user_data as module
from app.core.config import settings

TABLES = ("credit_balances", "subscriptions", "credit_ledger", "scans", "extensions", "suggestions")


def install(monkeypatch, fail_on=None):
    calls = []
    for name in TABLES:
        monkeypatch.setattr(settings, f"appwrite_{name}_table_id", f"{name}-table")

    def make(name):
        def step(user_id):
            calls.append((name, user_id))
            if name == fail_on:
                raise RuntimeError(f"{name} failed")

        return step

    monkeypatch.setattr(module, "delete_cv", make("cv"))
    monkeypatch.setattr(module, "delete_usage_row", make("usage"))
    monkeypatch.setattr(
        module, "delete_row_by_id", lambda table_id, row_id: calls.append((table_id, row_id))
    )
    monkeypatch.setattr(
        module, "delete_rows_by_user", lambda table_id, user_id: calls.append((table_id, user_id))
    )
    return calls


def test_deletes_everything_the_user_left_behind_but_not_payments_or_testimonials(monkeypatch):
    calls = install(monkeypatch)

    module.delete_user_data("user-1")

    assert calls == [
        ("cv", "user-1"),
        ("usage", "user-1"),
        ("credit_balances-table", "user-1"),
        ("subscriptions-table", "user-1"),
        ("credit_ledger-table", "user-1"),
        ("scans-table", "user-1"),
        ("extensions-table", "user-1"),
        ("suggestions-table", "user-1"),
    ]


def test_a_failing_step_raises_so_the_deletion_can_be_retried(monkeypatch):
    install(monkeypatch, fail_on="usage")

    with pytest.raises(RuntimeError):
        module.delete_user_data("user-1")
