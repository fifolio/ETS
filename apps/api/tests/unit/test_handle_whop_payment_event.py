from datetime import UTC, datetime

import app.services.payments.whop.handle_whop_payment_event as module
from tests.conftest import make_notice

NOW = datetime(2026, 12, 1, tzinfo=UTC)
DATA = {"id": "pay_1", "status": "paid"}


def install(monkeypatch, parsed=None, renewal=None):
    calls = []
    monkeypatch.setattr(module, "parse_whop_payment", lambda data, env: parsed)
    monkeypatch.setattr(module, "resolve_renewal_notice", lambda data, env: renewal)
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


def test_a_paid_payment_of_ours_is_applied(monkeypatch):
    calls = install(monkeypatch, parsed=make_notice())

    assert module.handle_whop_payment_event("payment.succeeded", DATA, "sandbox", NOW) == "applied"
    assert calls == [("apply", "pay_1")]


def test_a_renewal_without_metadata_is_applied_through_its_membership(monkeypatch):
    calls = install(monkeypatch, renewal=make_notice(sku="plan_nextmove"))

    assert module.handle_whop_payment_event("payment.succeeded", DATA, "sandbox", NOW) == "applied"
    assert calls == [("apply", "pay_1")]


def test_a_payment_that_is_not_ours_is_ignored(monkeypatch):
    calls = install(monkeypatch)

    assert module.handle_whop_payment_event("payment.succeeded", DATA, "sandbox", NOW) == "ignored"
    assert calls == []


def test_a_succeeded_event_that_is_not_paid_is_ignored(monkeypatch):
    calls = install(monkeypatch, parsed=make_notice())

    assert (
        module.handle_whop_payment_event(
            "payment.succeeded", {**DATA, "status": "open"}, "sandbox", NOW
        )
        == "ignored"
    )
    assert calls == []


def test_a_failed_payment_is_recorded(monkeypatch):
    calls = install(monkeypatch, parsed=make_notice())

    assert module.handle_whop_payment_event("payment.failed", DATA, "sandbox", NOW) == "failed"
    assert calls == [("failed", "pay_1")]
