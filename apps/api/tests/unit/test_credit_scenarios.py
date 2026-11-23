from datetime import UTC, datetime

import pytest

import app.services.credits.add_credits as add_module
import app.services.credits.apply_spend_steps as spend_module
import app.services.credits.ensure_credit_account as ensure_module
import app.services.credits.expire_monthly_credits as expire_module
import app.services.credits.reserve_credits as reserve_module
from app.services.credits.add_credits import add_credits
from app.services.credits.apply_plan_credits import apply_plan_credits
from app.services.credits.ensure_credit_account import ensure_credit_account
from app.services.credits.grant_topup_credits import grant_topup_credits
from app.services.credits.reserve_credits import reserve_credits
from app.types.credit_balance import CreditBalance

NOW = datetime(2026, 12, 1, tzinfo=UTC)
USER = "user-1"


class Store:
    """An in-memory credit system: balances plus a history with unique keys."""

    def __init__(self):
        self.balances = None  # None until the user's row exists
        self.keys = set()
        self.ledger = []
        self.has_row = False

    def get_credit_balance(self, user_id):
        return None if self.balances is None else CreditBalance(**self.balances)

    def increment_balance(self, user_id, kind, amount):
        if self.balances is None:
            self.balances = {"subscription": 0, "promotional": 0, "purchased": 0}
        self.balances[kind] += amount

    def decrement_balance(self, user_id, kind, amount):
        if self.balances is None or self.balances[kind] < amount:
            return False
        self.balances[kind] -= amount
        return True

    def write_ledger(self, user_id, amount, kind, reason, ref_id=None, idempotency_key=None):
        if idempotency_key and idempotency_key in self.keys:
            return None
        if idempotency_key:
            self.keys.add(idempotency_key)
        self.ledger.append((amount, kind, reason))
        return f"ledger-{len(self.ledger)}"

    def as_tuple(self):
        b = self.balances
        return (b["subscription"], b["promotional"], b["purchased"])


@pytest.fixture
def store(monkeypatch):
    s = Store()
    monkeypatch.setattr(add_module, "write_ledger", s.write_ledger)
    monkeypatch.setattr(add_module, "increment_balance", s.increment_balance)
    monkeypatch.setattr(expire_module, "get_credit_balance", s.get_credit_balance)
    monkeypatch.setattr(expire_module, "write_ledger", s.write_ledger)
    monkeypatch.setattr(expire_module, "decrement_balance", s.decrement_balance)
    monkeypatch.setattr(ensure_module, "has_subscription", lambda user_id: s.has_row)
    monkeypatch.setattr(
        ensure_module, "create_subscription_row", lambda *a: setattr(s, "has_row", True)
    )
    monkeypatch.setattr(reserve_module, "get_credit_balance", s.get_credit_balance)
    monkeypatch.setattr(reserve_module, "write_ledger", s.write_ledger)
    monkeypatch.setattr(spend_module, "decrement_balance", s.decrement_balance)
    monkeypatch.setattr(spend_module, "increment_balance", s.increment_balance)
    return s


def test_a_new_explore_user_gets_15_monthly_and_25_welcome_credits(store):
    ensure_credit_account(USER, NOW)

    assert store.as_tuple() == (15, 25, 0)


def test_a_new_next_move_user_gets_150_monthly_and_25_welcome_credits(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "nextmove", "p1")

    assert store.as_tuple() == (150, 25, 0)


def test_a_new_urgent_user_gets_300_monthly_and_25_welcome_credits(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "urgent", "p1")

    assert store.as_tuple() == (300, 25, 0)


def test_upgrading_from_explore_does_not_grant_another_welcome_bonus(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "nextmove", "p1")

    welcome_rows = [row for row in store.ledger if row[2] == "Welcome bonus"]
    assert len(welcome_rows) == 1 and store.balances["promotional"] == 25


def test_upgrading_to_urgent_replaces_the_monthly_credits_instead_of_stacking(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "nextmove", "p1")
    for _ in range(10):
        reserve_credits(USER)

    apply_plan_credits(USER, "urgent", "p2")

    assert store.as_tuple() == (300, 25, 0)


def test_a_payment_notification_repeated_for_the_same_period_changes_nothing(store):
    ensure_credit_account(USER, NOW)
    assert apply_plan_credits(USER, "nextmove", "p1") is True
    balances, rows = store.as_tuple(), len(store.ledger)

    assert apply_plan_credits(USER, "nextmove", "p1") is False
    assert store.as_tuple() == balances and len(store.ledger) == rows


def test_renewal_resets_the_monthly_credits_without_rolling_them_over(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "nextmove", "p1")
    for _ in range(110):
        reserve_credits(USER)
    assert store.balances["subscription"] == 40

    apply_plan_credits(USER, "nextmove", "p2")

    assert store.balances["subscription"] == 150


def test_a_top_up_adds_purchased_credits_once_and_leaves_the_plan_alone(store):
    ensure_credit_account(USER, NOW)
    apply_plan_credits(USER, "nextmove", "p1")

    assert grant_topup_credits(USER, 500, "pay_1") is True
    assert grant_topup_credits(USER, 500, "pay_1") is False

    assert store.as_tuple() == (150, 25, 40)


def test_invalid_credit_amounts_are_refused(store):
    with pytest.raises(ValueError):
        grant_topup_credits(USER, 0, "pay_2")
    with pytest.raises(ValueError):
        add_credits(USER, "purchased", -5, "Bad grant", "key-1")


def test_credits_are_spent_monthly_first_then_welcome_then_purchased(store):
    store.balances = {"subscription": 1, "promotional": 25, "purchased": 40}

    steps = reserve_credits(USER, 3)

    assert steps == [("subscription", 1), ("promotional", 2)]
    assert store.as_tuple() == (0, 23, 40)
