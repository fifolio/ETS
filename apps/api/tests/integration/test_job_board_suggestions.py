import pytest
from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.main import app
from app.types.authenticated_user import AuthenticatedUser

client = TestClient(app)

URL = "/job-board-suggestions"
PAYLOAD = {"name": "Wellfound", "url": "https://wellfound.com/jobs"}


def test_a_suggestion_is_accepted_and_reports_the_remaining_count(monkeypatch, logged_in):
    received = []

    def fake_submit(user_id, request, now):
        received.append((user_id, request.name, request.url))
        return 2

    monkeypatch.setattr("app.routers.job_board_suggestions.submit_suggestion", fake_submit)

    response = client.post(URL, json=PAYLOAD)

    assert response.status_code == 201
    assert response.json() == {"status": "pending", "remaining_today": 2}
    assert received == [("user-1", "Wellfound", "https://wellfound.com/jobs")]


@pytest.mark.parametrize(
    ("status", "message"),
    [
        (409, "LinkedIn is already supported."),
        (422, "Enter a valid web address."),
        (429, "You reached today's limit."),
    ],
)
def test_a_rejection_keeps_its_status_and_message(monkeypatch, logged_in, status, message):
    def reject(user_id, request, now):
        raise SuggestionRejectedError(message, status)

    monkeypatch.setattr("app.routers.job_board_suggestions.submit_suggestion", reject)

    response = client.post(URL, json=PAYLOAD)

    assert response.status_code == status
    assert response.json() == {"detail": message}


def test_a_request_without_a_name_is_rejected(logged_in):
    assert client.post(URL, json={"url": "https://wellfound.com/jobs"}).status_code == 422


def test_an_unverified_user_cannot_suggest(logged_in):
    unverified = AuthenticatedUser("user-2", "Jane Doe", "jane.doe@example.com", False)
    app.dependency_overrides[get_current_user] = lambda: unverified

    assert client.post(URL, json=PAYLOAD).status_code == 403


def test_suggesting_needs_a_login():
    assert client.post(URL, json=PAYLOAD).status_code == 401
