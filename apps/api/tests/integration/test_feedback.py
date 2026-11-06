import pytest
from fastapi.testclient import TestClient

from app.constants.feedback import MAX_QUOTE_LENGTH
from app.dependencies.get_current_user import get_current_user
from app.exceptions.feedback_already_submitted_error import FeedbackAlreadySubmittedError
from app.exceptions.feedback_not_available_error import FeedbackNotAvailableError
from app.main import app
from app.schemas.feedback_eligibility import FeedbackEligibility
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)

VALID = {
    "quote": "Saved me hours every week.",
    "internal_suggestions": "Add Safari.",
    "consent": True,
}


def raising(error):
    def fail(*args):
        raise error

    return fail


def test_eligibility_is_returned(monkeypatch, logged_in):
    result = FeedbackEligibility(
        eligible=True, trial_over=True, enough_scans=True, already_submitted=False
    )
    monkeypatch.setattr(
        "app.routers.feedback.eligibility.get_feedback_eligibility", lambda u, n: result
    )

    response = client.get("/feedback/eligibility")

    assert response.status_code == 200
    assert response.json()["eligible"] is True


def test_sending_feedback_returns_201(monkeypatch, logged_in):
    monkeypatch.setattr("app.routers.feedback.submit.submit_feedback", lambda *args: None)

    response = client.post("/feedback", json=VALID)

    assert response.status_code == 201
    assert response.json() == {"status": "pending"}


def test_feedback_that_is_not_available_yet_returns_403(monkeypatch, logged_in):
    monkeypatch.setattr(
        "app.routers.feedback.submit.submit_feedback", raising(FeedbackNotAvailableError())
    )

    assert client.post("/feedback", json=VALID).status_code == 403


def test_feedback_sent_twice_returns_409(monkeypatch, logged_in):
    monkeypatch.setattr(
        "app.routers.feedback.submit.submit_feedback", raising(FeedbackAlreadySubmittedError())
    )

    assert client.post("/feedback", json=VALID).status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {"quote": "x" * (MAX_QUOTE_LENGTH + 1), "consent": True},
        {"quote": "", "internal_suggestions": ""},
        {"quote": "Great tool", "consent": False},
    ],
)
def test_invalid_feedback_returns_422(logged_in, payload):
    assert client.post("/feedback", json=payload).status_code == 422


def test_unverified_users_cannot_send_feedback(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.post("/feedback", json=VALID).status_code == 403
