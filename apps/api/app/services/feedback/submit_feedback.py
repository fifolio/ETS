from contextlib import suppress
from datetime import datetime

from appwrite.exception import AppwriteException

from app.constants.account import FEEDBACK_DONE_LABEL
from app.constants.feedback import TESTIMONIAL_STATUS_PENDING
from app.exceptions.feedback_already_submitted_error import FeedbackAlreadySubmittedError
from app.exceptions.feedback_not_available_error import FeedbackNotAvailableError
from app.schemas.feedback_request import FeedbackRequest
from app.services.appwrite.add_user_label import add_user_label
from app.services.feedback.build_display_name import build_display_name
from app.services.feedback.compute_metrics import compute_metrics
from app.services.feedback.create_feedback_row import create_feedback_row
from app.services.feedback.get_feedback_eligibility import get_feedback_eligibility
from app.services.feedback.metrics_to_json import metrics_to_json
from app.types.authenticated_user import AuthenticatedUser
from app.types.feedback_row_data import FeedbackRowData


def submit_feedback(user: AuthenticatedUser, request: FeedbackRequest, now: datetime) -> None:
    """Store the feedback as a pending entry and mark the user as done."""
    if FEEDBACK_DONE_LABEL in user.labels:
        raise FeedbackAlreadySubmittedError
    if not get_feedback_eligibility(user, now).eligible:
        raise FeedbackNotAvailableError

    role = user.prefs.get("role")
    data: FeedbackRowData = {
        "userId": user.id,
        "quote": request.quote.strip(),
        "internalSuggestions": request.internal_suggestions.strip(),
        "metricsSaved": metrics_to_json(compute_metrics(user.id)),
        "displayName": build_display_name(user.name),
        "role": role if isinstance(role, str) else "",
        "consent": request.consent,
        "status": TESTIMONIAL_STATUS_PENDING,
    }
    try:
        create_feedback_row(data)
    except AppwriteException as exc:
        if exc.code == 409:  # the unique index on userId: this user already sent feedback
            with suppress(AppwriteException):
                add_user_label(user.id, user.labels, FEEDBACK_DONE_LABEL)
            raise FeedbackAlreadySubmittedError from exc
        raise
    add_user_label(user.id, user.labels, FEEDBACK_DONE_LABEL)
