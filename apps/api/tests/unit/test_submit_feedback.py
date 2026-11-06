from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from appwrite.exception import AppwriteException

import app.services.feedback.submit_feedback as module
from app.exceptions.feedback_already_submitted_error import FeedbackAlreadySubmittedError
from app.exceptions.feedback_not_available_error import FeedbackNotAvailableError
from app.schemas.feedback_eligibility import FeedbackEligibility
from app.schemas.feedback_request import FeedbackRequest
from app.types.authenticated_user import AuthenticatedUser
from app.types.feedback_metrics import FeedbackMetrics

NOW = datetime(2026, 11, 20, tzinfo=UTC)
REQUEST = FeedbackRequest(quote=" Great tool ", internal_suggestions="Add dark mode", consent=True)


def make_user(labels=None):
    return AuthenticatedUser(
        "user-1", "Jane Doe", "jane.doe@example.com", True, {"role": "Nurse"}, labels or []
    )


def eligibility(eligible=True):
    return FeedbackEligibility(
        eligible=eligible, trial_over=eligible, enough_scans=eligible, already_submitted=False
    )


@pytest.fixture
def env(monkeypatch):
    created, labeled = [], []
    monkeypatch.setattr(module, "get_feedback_eligibility", lambda user, now: eligibility())
    monkeypatch.setattr(module, "compute_metrics", lambda user_id: FeedbackMetrics(18, 9000, 40.0))
    monkeypatch.setattr(module, "create_feedback_row", created.append)
    monkeypatch.setattr(module, "add_user_label", lambda *args: labeled.append(args))
    return SimpleNamespace(created=created, labeled=labeled, monkeypatch=monkeypatch)


def test_stores_a_pending_row_with_a_snapshot_and_marks_the_user(env):
    module.submit_feedback(make_user(), REQUEST, NOW)

    row = env.created[0]
    assert row["status"] == "pending"
    assert row["quote"] == "Great tool"
    assert row["internalSuggestions"] == "Add dark mode"
    assert row["displayName"] == "Jane D."
    assert row["role"] == "Nurse"
    assert row["consent"] is True
    assert '"scans": 18' in row["metricsSaved"]
    assert env.labeled == [("user-1", [], "feedbackdone")]


def test_refuses_when_the_user_is_not_eligible(env):
    env.monkeypatch.setattr(module, "get_feedback_eligibility", lambda u, n: eligibility(False))

    with pytest.raises(FeedbackNotAvailableError):
        module.submit_feedback(make_user(), REQUEST, NOW)
    assert env.created == []


def test_refuses_when_feedback_was_already_sent(env):
    with pytest.raises(FeedbackAlreadySubmittedError):
        module.submit_feedback(make_user(labels=["feedbackdone"]), REQUEST, NOW)
    assert env.created == []


def test_a_duplicate_row_is_reported_and_the_label_is_repaired(env):
    def duplicate(data):
        raise AppwriteException("duplicate", 409)

    env.monkeypatch.setattr(module, "create_feedback_row", duplicate)

    with pytest.raises(FeedbackAlreadySubmittedError):
        module.submit_feedback(make_user(), REQUEST, NOW)
    assert env.labeled == [("user-1", [], "feedbackdone")]
