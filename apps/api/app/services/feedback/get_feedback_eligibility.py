from datetime import datetime

from app.constants.account import FEEDBACK_DONE_LABEL
from app.core.config import settings
from app.schemas.feedback_eligibility import FeedbackEligibility
from app.services.feedback.count_scans_up_to import count_scans_up_to
from app.services.feedback.is_trial_over import is_trial_over
from app.types.authenticated_user import AuthenticatedUser


def get_feedback_eligibility(user: AuthenticatedUser, now: datetime) -> FeedbackEligibility:
    already_submitted = FEEDBACK_DONE_LABEL in user.labels
    trial_over = is_trial_over(user.registered_at, now)
    enough_scans = (
        count_scans_up_to(user.id, settings.feedback_min_scans) >= settings.feedback_min_scans
    )
    return FeedbackEligibility(
        eligible=trial_over and enough_scans and not already_submitted,
        trial_over=trial_over,
        enough_scans=enough_scans,
        already_submitted=already_submitted,
    )
