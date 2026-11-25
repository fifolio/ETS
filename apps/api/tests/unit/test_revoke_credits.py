import app.services.credits.revoke_credits as module
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


def test_takes_the_credits_back_and_records_it(monkeypatch):
    ledger, taken = install(monkeypatch, CreditBalance(0, 0, 40))

    assert module.revoke_credits("user-1", "purchased", 40, "Refund", "refund:rf_1") == 40
    assert ledger == [("user-1", -40, "purchased", "Refund", None, "refund:rf_1")]
    assert taken == [("purchased", 40)]


def test_only_the_unspent_credits_are_taken_and_the_history_says_so(monkeypatch):
    ledger, taken = install(monkeypatch, CreditBalance(0, 0, 30))

    assert module.revoke_credits("user-1", "purchased", 40, "Refund", "refund:rf_1") == 30
    assert ledger[0][1] == -30 and "10 already used" in ledger[0][3]
    assert taken == [("purchased", 30)]


def test_a_refund_that_was_already_handled_takes_nothing(monkeypatch):
    _, taken = install(monkeypatch, CreditBalance(0, 0, 40), key_used=True)

    assert module.revoke_credits("user-1", "purchased", 40, "Refund", "refund:rf_1") == 0
    assert taken == []


def test_with_nothing_left_a_zero_row_is_written_and_nothing_is_taken(monkeypatch):
    ledger, taken = install(monkeypatch, CreditBalance(5, 0, 0))

    assert module.revoke_credits("user-1", "purchased", 40, "Refund", "refund:rf_1") == 0
    assert ledger[0][1] == 0 and taken == []
