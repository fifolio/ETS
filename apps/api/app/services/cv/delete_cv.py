from app.services.cv.delete_cv_file import delete_cv_file
from app.services.cv.delete_cv_row import delete_cv_row
from app.services.cv.get_cv import get_cv


def delete_cv(user_id: str) -> bool:
    """Delete the user's CV row and file. Returns False if there was no CV."""
    existing = get_cv(user_id)
    if existing is None:
        return False
    delete_cv_row(existing.row_id)
    if existing.file_id:
        delete_cv_file(existing.file_id)
    return True
