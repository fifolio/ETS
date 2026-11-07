from app.services.cv.create_cv_row import create_cv_row
from app.services.cv.get_cv import get_cv
from app.services.cv.update_cv_row import update_cv_row
from app.types.cv_row_data import CVRowData


def save_cv(user_id: str, file_name: str, text: str) -> None:
    """Store the CV text, replacing the user's previous CV. The PDF itself is not kept."""
    data: CVRowData = {"userId": user_id, "fileName": file_name, "text": text}
    existing = get_cv(user_id)
    if existing is None:
        create_cv_row(data)
    else:
        update_cv_row(existing.row_id, data)
