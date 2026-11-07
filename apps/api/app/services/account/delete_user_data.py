from app.services.cv.delete_cv import delete_cv
from app.services.scans.delete_user_scans import delete_user_scans
from app.services.usage.delete_usage_row import delete_usage_row


def delete_user_data(user_id: str) -> None:
    """Delete what the user left behind: the CV (row and file), usage totals, and scans.

    Testimonials are kept on purpose.
    """
    delete_cv(user_id)
    delete_usage_row(user_id)
    delete_user_scans(user_id)
