from datetime import datetime

from appwrite.exception import AppwriteException

from app.constants.suggestions import MAX_PENDING_SUGGESTIONS, MAX_SUGGESTIONS_PER_DAY
from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.schemas.job_board_suggestion_request import JobBoardSuggestionRequest
from app.services.job_boards.list_active_job_boards import list_active_job_boards
from app.services.suggestions.count_pending_suggestions import count_pending_suggestions
from app.services.suggestions.count_recent_suggestions import count_recent_suggestions
from app.services.suggestions.create_suggestion import create_suggestion
from app.services.suggestions.find_covering_board import find_covering_board
from app.services.suggestions.validate_suggestion import validate_suggestion


def submit_suggestion(user_id: str, request: JobBoardSuggestionRequest, now: datetime) -> int:
    """Store a job board suggestion. Returns how many more the user can send today."""
    suggestion = validate_suggestion(request)

    covering = find_covering_board(suggestion.url, list_active_job_boards())
    if covering is not None:
        raise SuggestionRejectedError(
            f"{covering.name} is already supported. Check Settings, Job boards.", 409
        )

    recent = count_recent_suggestions(user_id, now, MAX_SUGGESTIONS_PER_DAY)
    if recent >= MAX_SUGGESTIONS_PER_DAY:
        raise SuggestionRejectedError(
            "You reached today's limit of suggestions. Try again tomorrow.", 429
        )
    if count_pending_suggestions(user_id, MAX_PENDING_SUGGESTIONS) >= MAX_PENDING_SUGGESTIONS:
        raise SuggestionRejectedError(
            "You have many suggestions waiting for review. Please wait for some of them.", 429
        )

    try:
        create_suggestion(user_id, suggestion)
    except AppwriteException as exc:
        if exc.code == 409:  # the unique index on user and address
            raise SuggestionRejectedError("You already suggested this job board.", 409) from exc
        raise
    return max(0, MAX_SUGGESTIONS_PER_DAY - recent - 1)
