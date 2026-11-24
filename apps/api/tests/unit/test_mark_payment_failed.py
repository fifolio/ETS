from datetime import UTC, datetime

import app.services.payments.mark_payment_failed as module
from app.types.payment_rows import PaymentRows
from tests.conftest import make_notice, make_record

NOW = datetime(2026, 12, 1, tzinfo=UTC)


def install(monkeypatch, rows):
    saved = []
    monkeypatch.setattr(module, "resolve_payment_rows", lambda notice: rows)
    monkeypatch.setattr(
        module, "save_payment_result", lambda row, notice, result, now: saved.append((row, result))
    )
    return saved


def test_the_pending_checkout_row_becomes_failed_and_keeps_its_amounts(monkeypatch):
    pending = make_record()
    saved = install(monkeypatch, PaymentRows(None, pending, pending))

    assert module.mark_payment_failed(make_notice(), NOW) == "failed"

    row, result = saved[0]
    assert row == pending
    assert (result.status, result.applied, result.amount_cents, result.credits) == (
        "failed",
        False,
        500,
        40,
    )


def test_a_failure_nobody_recorded_creates_a_failed_row(monkeypatch):
    saved = install(monkeypatch, PaymentRows(None, None, None))

    assert module.mark_payment_failed(make_notice(), NOW) == "failed"

    assert saved[0][0] is None and saved[0][1].amount_cents == 0


def test_a_late_failure_notice_for_an_applied_payment_changes_nothing(monkeypatch):
    applied = make_record(payment_id="pay_1", applied=True, status="completed")
    saved = install(monkeypatch, PaymentRows(applied, applied, applied))

    assert module.mark_payment_failed(make_notice(), NOW) == "ignored"
    assert saved == []


def test_a_failed_attempt_on_the_payments_own_row_updates_that_row(monkeypatch):
    own = make_record(payment_id="pay_1")
    saved = install(monkeypatch, PaymentRows(own, own, own))

    module.mark_payment_failed(make_notice(), NOW)

    assert saved[0][0] == own
