from datetime import UTC, datetime

import pytest

import app.services.payments.apply_membership_update as module
from app.types.membership_notice import MembershipNotice
from tests.conftest import make_subscription

NOW = datetime(2026, 12, 20, tzinfo=UTC)
NEW_END = datetime(2027, 1, 30, tzinfo=UTC)


def notice(status="active", cancel=False, period_end=None):
    return MembershipNotice("whop", "mem_1", status, cancel, period_end)


def install(monkeypatch, record):
    calls = []
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: record)
    monkeypatch.setattr(
        module, "end_subscription", lambda rec, now: calls.append(("end", rec.user_id)) or "ended"
    )
    monkeypatch.setattr(
        module, "update_subscription_row", lambda user_id, data: calls.append(("row", data))
    )
    return calls


@pytest.mark.parametrize("status", ["canceled", "expired"])
def test_a_membership_that_ended_sends_the_user_back_to_explore(monkeypatch, status):
    calls = install(monkeypatch, make_subscription())

    assert module.apply_membership_update(notice(status), NOW) == "ended"
    assert calls == [("end", "user-1")]


def test_a_membership_that_is_not_the_users_current_one_is_ignored(monkeypatch):
    calls = install(monkeypatch, None)

    assert module.apply_membership_update(notice("canceled"), NOW) == "ignored"
    assert calls == []


def test_cancelling_at_period_end_is_recorded_and_the_plan_stays(monkeypatch):
    calls = install(monkeypatch, make_subscription())

    assert module.apply_membership_update(notice("active", cancel=True), NOW) == "updated"
    assert calls == [("row", {"cancelAtPeriodEnd": True})]


def test_a_new_period_end_is_stored_and_gets_a_new_reminder(monkeypatch):
    calls = install(monkeypatch, make_subscription())

    module.apply_membership_update(notice(period_end=NEW_END), NOW)

    row = calls[0][1]
    assert row["currentPeriodEnd"] == NEW_END.isoformat() and row["renewalReminderSentAt"] is None


def test_an_unchanged_period_end_keeps_the_reminder_that_was_sent(monkeypatch):
    record = make_subscription(period_end=NEW_END)
    calls = install(monkeypatch, record)

    module.apply_membership_update(notice(period_end=NEW_END), NOW)

    assert "renewalReminderSentAt" not in calls[0][1]


def test_other_statuses_are_ignored(monkeypatch):
    calls = install(monkeypatch, make_subscription())

    assert module.apply_membership_update(notice("drafted"), NOW) == "ignored"
    assert calls == []
