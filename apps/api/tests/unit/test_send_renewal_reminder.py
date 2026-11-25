from datetime import UTC, datetime

import app.services.subscriptions.send_renewal_reminder as module
from tests.conftest import make_subscription

NOW = datetime(2026, 12, 30, tzinfo=UTC)


def install(monkeypatch):
    calls = []
    monkeypatch.setattr(
        module,
        "send_notification",
        lambda user_id, kind, details: calls.append(("notify", kind, details)),
    )
    monkeypatch.setattr(
        module, "update_subscription_row", lambda user_id, data: calls.append(("row", data))
    )
    return calls


def test_a_renewing_plan_gets_a_renewing_reminder_and_is_marked(monkeypatch):
    calls = install(monkeypatch)

    module.send_renewal_reminder(make_subscription(), NOW)

    assert calls[0][1] == "subscription_renewing" and calls[0][2]["plan"] == "nextmove"
    assert calls[1] == ("row", {"renewalReminderSentAt": NOW.isoformat()})


def test_a_plan_that_is_cancelled_at_period_end_gets_an_ending_reminder(monkeypatch):
    calls = install(monkeypatch)

    module.send_renewal_reminder(make_subscription(cancel_at_period_end=True), NOW)

    assert calls[0][1] == "subscription_ending"
