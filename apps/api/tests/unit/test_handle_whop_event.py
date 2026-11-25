from datetime import UTC, datetime

import app.services.payments.whop.handle_whop_event as module

NOW = datetime(2026, 12, 1, tzinfo=UTC)


def install(monkeypatch):
    calls = []
    monkeypatch.setattr(
        module,
        "handle_whop_payment_event",
        lambda t, d, e, n: calls.append(("payment", t, d["id"])) or "applied",
    )
    monkeypatch.setattr(
        module,
        "apply_membership_update",
        lambda notice, now: calls.append(("membership", notice.membership_id)) or "updated",
    )
    monkeypatch.setattr(
        module,
        "apply_refund",
        lambda notice, now: calls.append(("refund", notice.refund_id)) or "refunded",
    )
    return calls


def test_payment_events_go_to_the_payment_handler(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event(
            {"type": "payment.succeeded", "data": {"id": "pay_1"}}, "sandbox", NOW
        )
        == "applied"
    )
    assert (
        module.handle_whop_event(
            {"type": "payment.failed", "data": {"id": "pay_2"}}, "sandbox", NOW
        )
        == "applied"
    )
    assert calls == [
        ("payment", "payment.succeeded", "pay_1"),
        ("payment", "payment.failed", "pay_2"),
    ]


def test_a_membership_update_is_applied(monkeypatch):
    calls = install(monkeypatch)

    event = {"type": "membership.updated", "data": {"id": "mem_1", "status": "canceled"}}

    assert module.handle_whop_event(event, "sandbox", NOW) == "updated"
    assert calls == [("membership", "mem_1")]


def test_refund_events_are_applied(monkeypatch):
    calls = install(monkeypatch)
    data = {"id": "rf_1", "payment": {"id": "pay_1"}}

    assert (
        module.handle_whop_event({"type": "refund.created", "data": data}, "sandbox", NOW)
        == "refunded"
    )
    assert (
        module.handle_whop_event({"type": "refund.updated", "data": data}, "sandbox", NOW)
        == "refunded"
    )
    assert calls == [("refund", "rf_1"), ("refund", "rf_1")]


def test_unreadable_membership_or_refund_data_is_ignored(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event({"type": "membership.updated", "data": {}}, "sandbox", NOW)
        == "ignored"
    )
    assert (
        module.handle_whop_event({"type": "refund.created", "data": {}}, "sandbox", NOW)
        == "ignored"
    )
    assert calls == []


def test_other_event_types_and_missing_data_are_ignored(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.handle_whop_event({"type": "member.created", "data": {"id": "x"}}, "sandbox", NOW)
        == "ignored"
    )
    assert module.handle_whop_event({"type": "payment.succeeded"}, "sandbox", NOW) == "ignored"
    assert calls == []
