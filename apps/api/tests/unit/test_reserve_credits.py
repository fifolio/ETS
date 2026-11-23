import app.services.credits.reserve_credits as module
from app.types.credit_balance import CreditBalance

BALANCE = CreditBalance(subscription=5, promotional=1, purchased=0)


def install(monkeypatch, balances, applies, ledger_error=None):
    ledger, reads, attempts = [], [], []
    balance_queue, apply_queue = list(balances), list(applies)

    def get_balance(user_id):
        reads.append(1)
        return balance_queue.pop(0) if len(balance_queue) > 1 else balance_queue[0]

    def apply(user_id, steps):
        attempts.append(steps)
        return apply_queue.pop(0) if len(apply_queue) > 1 else apply_queue[0]

    def write(*args):
        if ledger_error:
            raise ledger_error
        ledger.append(args)

    monkeypatch.setattr(module, "get_credit_balance", get_balance)
    monkeypatch.setattr(module, "apply_spend_steps", apply)
    monkeypatch.setattr(module, "write_ledger", write)
    return ledger, reads, attempts


def test_spends_a_credit_and_records_it_in_the_history(monkeypatch):
    ledger, _, attempts = install(monkeypatch, [BALANCE], [True])

    assert module.reserve_credits("user-1") == [("subscription", 1)]
    assert attempts == [[("subscription", 1)]]
    assert ledger == [("user-1", -1, "subscription", "Job scan")]


def test_not_enough_credits_spends_nothing(monkeypatch):
    _, _, attempts = install(monkeypatch, [CreditBalance(1, 1, 1)], [True])

    assert module.reserve_credits("user-1", 4) is None
    assert attempts == []


def test_a_user_without_a_balance_row_cannot_spend(monkeypatch):
    _, _, attempts = install(monkeypatch, [None], [True])

    assert module.reserve_credits("user-1") is None
    assert attempts == []


def test_reads_the_balance_again_and_retries_when_a_concurrent_spend_got_there_first(monkeypatch):
    _, reads, _ = install(monkeypatch, [BALANCE, BALANCE], [False, True])

    assert module.reserve_credits("user-1") is not None
    assert len(reads) == 2


def test_gives_up_after_too_many_attempts(monkeypatch):
    monkeypatch.setattr(module, "MAX_SPEND_ATTEMPTS", 2)
    _, _, attempts = install(monkeypatch, [BALANCE], [False])

    assert module.reserve_credits("user-1") is None
    assert len(attempts) == 2


def test_a_failing_history_write_does_not_undo_the_spend(monkeypatch):
    install(monkeypatch, [BALANCE], [True], ledger_error=RuntimeError("ledger down"))

    assert module.reserve_credits("user-1") is not None
