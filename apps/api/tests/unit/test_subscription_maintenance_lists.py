from datetime import UTC, datetime, timedelta

import app.services.subscriptions.list_due_explore_renewals as due_module
import app.services.subscriptions.list_expired_paid_subscriptions as expired_module
import app.services.subscriptions.list_renewal_reminders as reminder_module
from tests.conftest import make_subscription

NOW = datetime(2027, 1, 15, 12, 0, tzinfo=UTC)


def capture(monkeypatch, module, records):
    seen = {}

    def fake(queries):
        seen["queries"] = " ".join(queries)
        return records

    monkeypatch.setattr(module, "list_subscription_records", fake)
    return seen


def test_explore_accounts_are_due_after_30_days(monkeypatch):
    seen = capture(monkeypatch, due_module, [make_subscription(plan="explore")])

    result = due_module.list_due_explore_renewals(NOW)

    assert len(result) == 1
    assert (
        "explore" in seen["queries"] and (NOW - timedelta(days=30)).isoformat() in seen["queries"]
    )


def test_paid_plans_are_expired_7_days_after_their_period_end_and_explore_is_left_alone(
    monkeypatch,
):
    seen = capture(
        monkeypatch, expired_module, [make_subscription(), make_subscription(plan="explore")]
    )

    result = expired_module.list_expired_paid_subscriptions(NOW)

    assert [r.plan for r in result] == ["nextmove"]
    assert (NOW - timedelta(days=7)).isoformat() in seen["queries"]


def test_reminders_cover_the_next_24_hours(monkeypatch):
    seen = capture(monkeypatch, reminder_module, [make_subscription()])

    assert len(reminder_module.list_renewal_reminders(NOW)) == 1
    assert (NOW + timedelta(hours=24)).isoformat() in seen["queries"]


def test_a_reminder_is_not_sent_twice_and_not_to_explore(monkeypatch):
    records = [
        make_subscription(reminder_sent_at=NOW),
        make_subscription(plan="explore"),
        make_subscription(user_id="user-2"),
    ]
    capture(monkeypatch, reminder_module, records)

    assert [r.user_id for r in reminder_module.list_renewal_reminders(NOW)] == ["user-2"]
