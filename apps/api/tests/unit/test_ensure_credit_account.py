from datetime import UTC, datetime

import pytest

import app.services.credits.ensure_credit_account as module

NOW = datetime(2026, 11, 21, 12, 0, tzinfo=UTC)


def install(monkeypatch, has_row, grant_error=None):
    calls = []

    def grant(*args):
        if grant_error:
            raise grant_error
        calls.append(("grant", args))

    monkeypatch.setattr(module, "has_subscription", lambda user_id: has_row)
    monkeypatch.setattr(module, "add_credits", grant)
    monkeypatch.setattr(
        module, "create_subscription_row", lambda *args: calls.append(("row", args))
    )
    return calls


def test_a_user_with_a_subscription_row_gets_nothing_new(monkeypatch):
    calls = install(monkeypatch, has_row=True)

    module.ensure_credit_account("user-1", NOW)

    assert calls == []


def test_a_new_user_gets_the_explore_credits_and_then_the_row(monkeypatch):
    calls = install(monkeypatch, has_row=False)

    module.ensure_credit_account("user-1", NOW)

    assert calls == [
        ("grant", ("user-1", "promotional", 25, "Welcome bonus", "welcome:user-1")),
        ("grant", ("user-1", "subscription", 15, "Explore credits", "explore-init:user-1")),
        ("row", ("user-1", "explore", NOW)),
    ]


def test_a_failing_grant_leaves_no_row_so_the_next_call_tries_again(monkeypatch):
    calls = install(monkeypatch, has_row=False, grant_error=RuntimeError("table down"))

    with pytest.raises(RuntimeError):
        module.ensure_credit_account("user-1", NOW)
    assert calls == []
