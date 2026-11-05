from app.constants.account import CV_DONE_LABEL
from app.services.appwrite.add_user_label import add_user_label
from app.types.authenticated_user import AuthenticatedUser


def mark_cv_done(user: AuthenticatedUser) -> None:
    """Mark the user's CV as done by adding the CV_DONE_LABEL to their labels."""
    if CV_DONE_LABEL in user.labels:
        return
    add_user_label(user.id, user.labels, CV_DONE_LABEL)
