from datetime import UTC, datetime

import app.services.payments.apply_payment as module
from app.types.payment_rows import PaymentRows
from tests.conftest import make_notice, make_record

NOW = datetime(2026, 12, 1, tzinfo=UTC)


def install(monkeypatch, rows=None, user_exists=True):
    calls = []
    rows = rows or PaymentRows(None, None, None)
    monkeypatch.setattr(module, "resolve_payment_rows", lambda notice: rows)
    monkeypatch.setattr(module, "user_exists", lambda user_id: user_exists)
    monkeypatch.setattr(
        module, "ensure_credit_account", lambda user_id, now: calls.append(("ensure", user_id))
    )
    monkeypatch.setattr(module, "grant_topup_credits", lambda *args: calls.append(("topup", args)))
    monkeypatch.setattr(
        module, "activate_plan", lambda notice, plan_id, now: calls.append(("plan", plan_id))
    )
    monkeypatch.setattr(
        module,
        "save_payment_result",
        lambda row, notice, result, now: calls.append(("save", row, result)),
    )
    monkeypatch.setattr(
        module,
        "reject_payment",
        lambda row, notice, verdict, now: (
            calls.append(("reject", verdict.outcome)) or verdict.outcome
        ),
    )
    return calls


def test_a_payment_that_was_already_applied_is_a_duplicate(monkeypatch):
    applied = make_record(payment_id="pay_1", applied=True)
    calls = install(monkeypatch, PaymentRows(applied, applied, applied))

    assert module.apply_payment(make_notice(), NOW) == "duplicate"
    assert calls == []


def test_a_top_up_creates_the_credit_account_then_grants_exactly_its_credits(monkeypatch):
    record = make_record(amount_cents=500)
    calls = install(monkeypatch, PaymentRows(None, record, record))

    assert module.apply_payment(make_notice(paid_cents=500), NOW) == "applied"

    assert calls[0] == ("ensure", "user-1")
    assert calls[1] == ("topup", ("user-1", 500, "pay_1"))
    _, row, result = calls[2]
    assert row == record
    assert (result.amount_cents, result.credits, result.status, result.applied) == (
        500,
        40,
        "completed",
        True,
    )


def test_a_plan_payment_activates_the_plan_with_its_monthly_credits(monkeypatch):
    calls = install(monkeypatch)

    assert module.apply_payment(make_notice(sku="plan_nextmove", paid_cents=700), NOW) == "applied"

    assert [call[0] for call in calls] == ["ensure", "plan", "save"]
    assert calls[1] == ("plan", "nextmove")
    assert (calls[2][2].amount_cents, calls[2][2].credits) == (700, 150)


def test_an_underpaid_payment_grants_nothing(monkeypatch):
    record = make_record(amount_cents=500)
    calls = install(monkeypatch, PaymentRows(None, record, record))

    assert module.apply_payment(make_notice(paid_cents=400), NOW) == "underpaid"
    assert calls == [("reject", "underpaid")]


def test_a_payment_for_a_deleted_account_grants_nothing_and_creates_no_credit_rows(monkeypatch):
    calls = install(monkeypatch, user_exists=False)

    assert module.apply_payment(make_notice(), NOW) == "unknown_user"
    assert calls == [("reject", "unknown_user")]


def test_an_unknown_plan_grants_nothing(monkeypatch):
    calls = install(monkeypatch)

    assert module.apply_payment(make_notice(sku="plan_platinum"), NOW) == "invalid_amount"
    assert calls == [("reject", "invalid_amount")]
