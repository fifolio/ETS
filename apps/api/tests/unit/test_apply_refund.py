from datetime import UTC, datetime

import app.services.payments.apply_refund as module
from app.types.refund_notice import RefundNotice
from tests.conftest import make_record, make_subscription

NOW = datetime(2026, 12, 20, tzinfo=UTC)


def refund(amount=500, status="succeeded", membership="mem_1", refund_id="rf_1"):
    return RefundNotice("whop", refund_id, "pay_1", membership, amount, status)


def install(monkeypatch, row):
    calls = []
    monkeypatch.setattr(module, "find_payment_row", lambda column, value: row)
    monkeypatch.setattr(module, "revoke_credits", lambda *args: calls.append(("revoke", args)))
    monkeypatch.setattr(
        module, "update_payment_row", lambda row_id, data: calls.append(("row", data))
    )
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: make_subscription())
    monkeypatch.setattr(
        module, "end_subscription", lambda record, now: calls.append(("end", record.user_id))
    )
    return calls


def applied_topup(**kw):
    return make_record(sku="topup", payment_id="pay_1", amount_cents=500, applied=True, **kw)


def test_a_full_refund_of_a_top_up_takes_back_its_credits_and_marks_the_payment_refunded(
    monkeypatch,
):
    calls = install(monkeypatch, applied_topup())

    assert module.apply_refund(refund(500), NOW) == "refunded"

    assert calls[0] == (
        "revoke",
        ("user-1", "purchased", 40, "Refund of a credit top-up", "refund:rf_1"),
    )
    assert calls[1] == ("row", {"status": "refunded"})


def test_a_partial_refund_takes_back_proportional_credits_and_keeps_the_payment(monkeypatch):
    calls = install(monkeypatch, applied_topup())

    module.apply_refund(refund(250), NOW)

    assert calls == [
        ("revoke", ("user-1", "purchased", 20, "Refund of a credit top-up", "refund:rf_1"))
    ]


def test_a_refund_does_not_revoke_credits_again_after_the_payment_is_refunded(monkeypatch):
    calls = install(monkeypatch, applied_topup(status="refunded"))

    assert module.apply_refund(refund(refund_id="rf_2"), NOW) == "duplicate"
    assert calls == []


def test_a_refund_that_is_still_pending_is_ignored(monkeypatch):
    calls = install(monkeypatch, applied_topup())

    assert module.apply_refund(refund(500, status="pending"), NOW) == "ignored"
    assert calls == []


def test_a_refund_of_a_payment_that_was_never_applied_is_ignored(monkeypatch):
    calls = install(monkeypatch, make_record(sku="topup", applied=False))

    assert module.apply_refund(refund(), NOW) == "ignored"
    assert calls == []


def test_a_refund_of_an_unknown_payment_is_ignored(monkeypatch):
    calls = install(monkeypatch, None)

    assert module.apply_refund(refund(), NOW) == "ignored"
    assert calls == []


def test_a_full_refund_of_a_plan_payment_ends_the_subscription(monkeypatch):
    row = make_record(sku="plan_nextmove", payment_id="pay_1", amount_cents=700, applied=True)
    calls = install(monkeypatch, row)

    module.apply_refund(refund(700), NOW)

    assert calls[0] == ("end", "user-1")
    assert ("row", {"status": "refunded"}) in calls
