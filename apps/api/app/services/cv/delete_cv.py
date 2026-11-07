from app.services.cv.delete_cv_row import delete_cv_row
from app.services.cv.get_cv import get_cv


def delete_cv(user_id: str) -> bool:
    """Delete the user's CV. Returns False if there was none."""
    existing = get_cv(user_id)
    if existing is None:
        return False
    delete_cv_row(existing.row_id)
    return True
