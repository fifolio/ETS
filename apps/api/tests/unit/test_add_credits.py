import pytest

import app.services.credits.add_credits as module


def install(monkeypatch, ledger_id="ledger-1", increment_error=None):
    calls = []

    def ledger(*args):
        calls.append(("ledger", args))
        return ledger_id

    def increment(user_id, kind, amount):
        if increment_error:
            raise increment_error
        calls.append(("increment", (user_id, kind, amount)))

    monkeypatch.setattr(module, "write_ledger", ledger)
    monkeypatch.setattr(module, "increment_balance", increment)
    monkeypatch.setattr(
        module, "delete_ledger_row", lambda row_id: calls.append(("delete", row_id))
    )
    return calls


def test_a_grant_is_written_to_the_ledger_first_and_then_added_to_the_balance(monkeypatch):
    calls = install(monkeypatch)

    assert module.add_credits("user-1", "promotional", 25, "Bonus", "key-1") is True

    assert calls == [
        ("ledger", ("user-1", 25, "promotional", "Bonus", None, "key-1")),
        ("increment", ("user-1", "promotional", 25)),
    ]


def test_a_key_that_was_already_used_grants_nothing(monkeypatch):
    calls = install(monkeypatch, ledger_id=None)

    assert module.add_credits("user-1", "promotional", 25, "Bonus", "key-1") is False
    assert [name for name, _ in calls] == ["ledger"]


def test_a_failing_balance_update_frees_the_key_and_raises(monkeypatch):
    calls = install(monkeypatch, increment_error=RuntimeError("table down"))

    with pytest.raises(RuntimeError):
        module.add_credits("user-1", "purchased", 25, "Top-up", "key-1")
    assert ("delete", "ledger-1") in calls


def test_an_unknown_kind_is_refused_before_anything_is_written(monkeypatch):
    calls = install(monkeypatch)

    with pytest.raises(ValueError):
        module.add_credits("user-1", "gift", 25, "Bonus", "key-1")
    assert calls == []


@pytest.mark.parametrize("amount", [0, -5])
def test_the_amount_must_be_positive(monkeypatch, amount):
    install(monkeypatch)

    with pytest.raises(ValueError):
        module.add_credits("user-1", "purchased", amount, "Top-up", "key-1")
