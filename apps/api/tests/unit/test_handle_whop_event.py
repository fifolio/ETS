from datetime import UTC, datetime

import app.services.payments.whop.handle_whop_event as module

NOW = datetime(2026, 12, 1, tzinfo=UTC)
DATA = {
    "id": "pay_1",
    "status": "paid",
    "currency": "usd",
    "total": {"amount": "5.00"},
    "metadata": {"ets_user_id": "user-1", "ets_sku": "topup"},
}


def install(monkeypatch):
    calls = []
    monkeypatch.setattr(
        module,
        "apply_payment",
        lambda notice, now: calls.append(("apply", notice.payment_id)) or "applied",
    )
    monkeypatch.setattr(
        module,
        "mark_payment_failed",
        lambda notice, now: calls.append(("failed", notice.payment_id)) or "failed",
    )
    return calls


def test_a_paid_payment_is_applied(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event({"type": "payment.succeeded", "data": DATA}, "sandbox", NOW)
        == "applied"
    )
    assert calls == [("apply", "pay_1")]


def test_a_succeeded_event_that_is_not_paid_is_ignored(monkeypatch):
    calls = install(monkeypatch)

    event = {"type": "payment.succeeded", "data": {**DATA, "status": "open"}}

    assert module.handle_whop_event(event, "sandbox", NOW) == "ignored"
    assert calls == []


def test_a_payment_that_is_not_one_of_ours_is_ignored(monkeypatch):
    calls = install(monkeypatch)

    event = {"type": "payment.succeeded", "data": {**DATA, "metadata": {}}}

    assert module.handle_whop_event(event, "sandbox", NOW) == "ignored"
    assert calls == []


def test_a_failed_payment_is_recorded(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event({"type": "payment.failed", "data": DATA}, "sandbox", NOW)
        == "failed"
    )
    assert calls == [("failed", "pay_1")]


def test_other_event_types_are_ignored(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event({"type": "membership.activated", "data": DATA}, "sandbox", NOW)
        == "ignored"
    )
    assert calls == []


def test_an_event_without_data_is_ignored(monkeypatch):
    install(monkeypatch)

    assert module.handle_whop_event({"type": "payment.succeeded"}, "sandbox", NOW) == "ignored"
