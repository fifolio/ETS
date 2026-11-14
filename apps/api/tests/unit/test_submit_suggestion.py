from datetime import UTC, datetime

import pytest
from appwrite.exception import AppwriteException

import app.services.suggestions.submit_suggestion as module
from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.schemas.job_board_suggestion_request import JobBoardSuggestionRequest
from app.types.job_board import JobBoard

NOW = datetime(2026, 11, 13, 12, 0, tzinfo=UTC)
LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")
REQUEST = JobBoardSuggestionRequest(name="Wellfound", url="https://wellfound.com/jobs")


def install(monkeypatch, recent=0, pending=0, create_error=None):
    created, calls = [], []

    def count_recent(user_id, now, limit):
        calls.append("recent")
        return recent

    def count_pending(user_id, limit):
        calls.append("pending")
        return pending

    def create(user_id, suggestion):
        if create_error:
            raise create_error
        created.append((user_id, suggestion))

    monkeypatch.setattr(module, "list_active_job_boards", lambda: [LINKEDIN])
    monkeypatch.setattr(module, "count_recent_suggestions", count_recent)
    monkeypatch.setattr(module, "count_pending_suggestions", count_pending)
    monkeypatch.setattr(module, "create_suggestion", create)
    return created, calls


def test_a_valid_suggestion_is_stored_and_the_remaining_count_is_returned(monkeypatch):
    created, _ = install(monkeypatch)

    remaining = module.submit_suggestion("user-1", REQUEST, NOW)

    assert remaining == 2
    assert created[0][0] == "user-1" and created[0][1].url == "https://wellfound.com/jobs"


def test_the_remaining_count_goes_down_with_earlier_suggestions(monkeypatch):
    install(monkeypatch, recent=1)

    assert module.submit_suggestion("user-1", REQUEST, NOW) == 1


def test_a_board_that_is_already_supported_is_refused_before_any_limit_check(monkeypatch):
    created, calls = install(monkeypatch)
    request = JobBoardSuggestionRequest(
        name="LinkedIn jobs", url="https://www.linkedin.com/jobs/search"
    )

    with pytest.raises(SuggestionRejectedError) as error:
        module.submit_suggestion("user-1", request, NOW)

    assert error.value.status_code == 409 and "LinkedIn" in error.value.message
    assert created == [] and calls == []


def test_an_invalid_suggestion_is_refused_before_anything_is_read(monkeypatch):
    created, calls = install(monkeypatch)
    request = JobBoardSuggestionRequest(name="x", url="https://wellfound.com/jobs")

    with pytest.raises(SuggestionRejectedError) as error:
        module.submit_suggestion("user-1", request, NOW)

    assert error.value.status_code == 422
    assert created == [] and calls == []


def test_the_daily_limit_is_enforced(monkeypatch):
    created, _ = install(monkeypatch, recent=3)

    with pytest.raises(SuggestionRejectedError) as error:
        module.submit_suggestion("user-1", REQUEST, NOW)

    assert error.value.status_code == 429 and created == []


def test_too_many_pending_suggestions_are_refused(monkeypatch):
    created, _ = install(monkeypatch, pending=10)

    with pytest.raises(SuggestionRejectedError) as error:
        module.submit_suggestion("user-1", REQUEST, NOW)

    assert error.value.status_code == 429 and created == []


def test_suggesting_the_same_board_twice_is_a_conflict(monkeypatch):
    install(monkeypatch, create_error=AppwriteException("duplicate", 409))

    with pytest.raises(SuggestionRejectedError) as error:
        module.submit_suggestion("user-1", REQUEST, NOW)

    assert error.value.status_code == 409 and "already suggested" in error.value.message


def test_other_storage_errors_are_raised(monkeypatch):
    install(monkeypatch, create_error=AppwriteException("boom", 500))

    with pytest.raises(AppwriteException):
        module.submit_suggestion("user-1", REQUEST, NOW)
