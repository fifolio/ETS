import app.services.credits.expire_monthly_credits as module
from app.types.credit_balance import CreditBalance


def install(monkeypatch, balance, key_used=False):
    ledger, taken = [], []

    def write(*args):
        if key_used:
            return None
        ledger.append(args)
        return "ledger-1"

    monkeypatch.setattr(module, "get_credit_balance", lambda user_id: balance)
    monkeypatch.setattr(module, "write_ledger", write)
    monkeypatch.setattr(
        module,
        "decrement_balance",
        lambda user_id, kind, amount: taken.append((kind, amount)) or True,
    )
    return ledger, taken


def test_the_leftover_expires_and_is_written_to_the_history(monkeypatch):
    ledger, taken = install(monkeypatch, CreditBalance(40, 25, 10))

    module.expire_monthly_credits("user-1", "key-1")

    assert ledger == [
        ("user-1", -40, "subscription", "Unused monthly credits expired", None, "key-1")
    ]
    assert taken == [("subscription", 40)]


def test_nothing_is_written_when_nothing_is_left(monkeypatch):
    ledger, taken = install(monkeypatch, CreditBalance(0, 25, 10))

    module.expire_monthly_credits("user-1", "key-1")

    assert ledger == [] and taken == []


def test_a_period_that_was_already_expired_changes_nothing(monkeypatch):
    _, taken = install(monkeypatch, CreditBalance(40, 25, 10), key_used=True)

    module.expire_monthly_credits("user-1", "key-1")

    assert taken == []
