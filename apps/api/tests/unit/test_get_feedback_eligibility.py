from datetime import UTC, datetime, timedelta

import pytest

import app.services.feedback.get_feedback_eligibility as module
from app.core.config import settings
from app.types.authenticated_user import AuthenticatedUser

NOW = datetime(2026, 11, 20, tzinfo=UTC)


@pytest.fixture(autouse=True)
def rules(monkeypatch):
    monkeypatch.setattr(settings, "feedback_min_days", 15)
    monkeypatch.setattr(settings, "feedback_min_scans", 15)


def make_user(days_old=20, labels=None):
    return AuthenticatedUser(
        "user-1",
        "Jane Doe",
        "jane.doe@example.com",
        True,
        {},
        labels or [],
        registered_at=NOW - timedelta(days=days_old),
    )


def with_scans(monkeypatch, count):
    monkeypatch.setattr(module, "count_scans_up_to", lambda user_id, limit: count)


def test_eligible_when_all_three_conditions_are_met(monkeypatch):
    with_scans(monkeypatch, 15)
    assert module.get_feedback_eligibility(make_user(), NOW).eligible is True


def test_not_eligible_before_the_trial_is_over(monkeypatch):
    with_scans(monkeypatch, 15)
    result = module.get_feedback_eligibility(make_user(days_old=10), NOW)

    assert result.eligible is False
    assert result.trial_over is False


def test_not_eligible_with_too_few_scans(monkeypatch):
    with_scans(monkeypatch, 14)
    result = module.get_feedback_eligibility(make_user(), NOW)

    assert result.eligible is False
    assert result.enough_scans is False


def test_not_eligible_after_feedback_was_sent(monkeypatch):
    with_scans(monkeypatch, 30)
    result = module.get_feedback_eligibility(make_user(labels=["feedbackdone"]), NOW)

    assert result.eligible is False
    assert result.already_submitted is True
