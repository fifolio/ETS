from datetime import UTC, datetime

import app.services.payments.reject_payment as module
from app.types.payment_verdict import PaymentVerdict
from tests.conftest import make_notice, make_record

NOW = datetime(2026, 12, 1, tzinfo=UTC)


def test_records_the_refusal_and_returns_why(monkeypatch):
    saved = []
    monkeypatch.setattr(module, "save_payment_result", lambda *args: saved.append(args))
    row = make_record()

    outcome = module.reject_payment(
        row, make_notice(), PaymentVerdict("mismatch", "failed", 0), NOW
    )

    assert outcome == "mismatch"
    saved_row, _, result, _ = saved[0]
    assert saved_row == row
    assert (result.status, result.applied, result.credits) == ("failed", False, 0)


def test_an_underpaid_payment_keeps_the_expected_amount(monkeypatch):
    saved = []
    monkeypatch.setattr(module, "save_payment_result", lambda *args: saved.append(args))

    module.reject_payment(None, make_notice(), PaymentVerdict("underpaid", "underpaid", 500), NOW)

    assert (saved[0][2].amount_cents, saved[0][2].status) == (500, "underpaid")
