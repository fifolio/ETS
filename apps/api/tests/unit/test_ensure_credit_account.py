from datetime import UTC, datetime

import app.services.credits.ensure_credit_account as module
from app.types.credit_balance import CreditBalance

NOW = datetime(2026, 11, 20, 12, 0, tzinfo=UTC)


def install(monkeypatch, balance):
    calls = []
    monkeypatch.setattr(module, "get_credit_balance", lambda user_id: balance)
    monkeypatch.setattr(
        module, "create_subscription_row", lambda *args: calls.append(("subscription_row", args))
    )
    monkeypatch.setattr(module, "add_credits", lambda *args: calls.append(("grant", args)))
    return calls


def test_a_user_who_already_has_a_balance_gets_nothing_new(monkeypatch):
    calls = install(monkeypatch, CreditBalance(0, 0, 0))

    module.ensure_credit_account("user-1", NOW)

    assert calls == []


def test_a_new_user_gets_an_explore_subscription_and_15_credits_once(monkeypatch):
    calls = install(monkeypatch, None)

    module.ensure_credit_account("user-1", NOW)

    assert calls == [
        ("subscription_row", ("user-1", "explore", NOW)),
        ("grant", ("user-1", "subscription", 15, "Explore credits", "explore-init:user-1")),
    ]
