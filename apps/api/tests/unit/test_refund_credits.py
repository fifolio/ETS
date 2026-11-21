import app.services.credits.refund_credits as module

STEPS = [("promotional", 1), ("subscription", 2)]


def install(monkeypatch, failing_kind=None, ledger_error=None):
    balance, ledger = [], []

    def increment(user_id, kind, amount):
        if kind == failing_kind:
            raise RuntimeError("table down")
        balance.append((kind, amount))

    def write(*args):
        if ledger_error:
            raise ledger_error
        ledger.append(args)

    monkeypatch.setattr(module, "increment_balance", increment)
    monkeypatch.setattr(module, "write_ledger", write)
    return balance, ledger


def test_gives_back_each_credit_and_records_it_in_the_history(monkeypatch):
    balance, ledger = install(monkeypatch)

    module.refund_credits("user-1", STEPS)

    assert balance == STEPS
    assert ledger == [
        ("user-1", 1, "promotional", "Refund: the scan failed"),
        ("user-1", 2, "subscription", "Refund: the scan failed"),
    ]


def test_a_failing_refund_is_skipped_without_stopping_the_others(monkeypatch):
    balance, ledger = install(monkeypatch, failing_kind="promotional")

    module.refund_credits("user-1", STEPS)

    assert balance == [("subscription", 2)]
    assert [entry[2] for entry in ledger] == ["subscription"]


def test_a_failing_history_write_never_raises(monkeypatch):
    install(monkeypatch, ledger_error=RuntimeError("ledger down"))

    module.refund_credits("user-1", STEPS)
