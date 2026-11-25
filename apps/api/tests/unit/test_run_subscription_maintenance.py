from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

import app.services.subscriptions.run_subscription_maintenance as module
from tests.conftest import make_subscription

NOW = datetime(2027, 1, 15, tzinfo=UTC)


@pytest.fixture
def env(monkeypatch):
    done = SimpleNamespace(renewed=[], ended=[], reminded=[])
    monkeypatch.setattr(
        module,
        "list_due_explore_renewals",
        lambda now: [make_subscription(user_id="e1", plan="explore")],
    )
    monkeypatch.setattr(
        module, "list_expired_paid_subscriptions", lambda now: [make_subscription(user_id="p1")]
    )
    monkeypatch.setattr(
        module, "list_renewal_reminders", lambda now: [make_subscription(user_id="r1")]
    )
    monkeypatch.setattr(
        module, "renew_explore_credits", lambda record, now: done.renewed.append(record.user_id)
    )
    monkeypatch.setattr(
        module, "end_subscription", lambda record, now: done.ended.append(record.user_id)
    )
    monkeypatch.setattr(
        module, "send_renewal_reminder", lambda record, now: done.reminded.append(record.user_id)
    )
    return done


def test_a_dry_run_reports_what_is_due_and_does_nothing(env):
    result = module.run_subscription_maintenance(NOW, dry_run=True)

    assert (result.explore_renewals_due, result.expired_due, result.reminders_due) == (1, 1, 1)
    assert (result.explore_renewed, result.ended, result.reminded) == (0, 0, 0)
    assert env.renewed == env.ended == env.reminded == []


def test_a_real_run_renews_ends_and_reminds(env):
    result = module.run_subscription_maintenance(NOW, dry_run=False)

    assert (env.renewed, env.ended, env.reminded) == (["e1"], ["p1"], ["r1"])
    assert (result.explore_renewed, result.ended, result.reminded, result.failed) == (1, 1, 1, 0)


def test_one_failure_is_counted_and_the_rest_still_run(env, monkeypatch):
    def fail(record, now):
        raise RuntimeError("table down")

    monkeypatch.setattr(module, "end_subscription", fail)

    result = module.run_subscription_maintenance(NOW, dry_run=False)

    assert (result.failed, result.ended, result.explore_renewed, result.reminded) == (1, 0, 1, 1)
