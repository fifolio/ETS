from app.services.cv.create_cv_row import create_cv_row
from app.services.cv.delete_cv_file import delete_cv_file
from app.services.cv.get_cv import get_cv
from app.services.cv.update_cv_row import update_cv_row
from app.services.cv.upload_cv_file import upload_cv_file
from app.types.cv_row_data import CVRowData


def save_cv(user_id: str, file_name: str, pdf_bytes: bytes, text: str) -> None:
    """Store the PDF and its text. Replaces the user's previous CV if there is one."""
    existing = get_cv(user_id)
    file_id = upload_cv_file(pdf_bytes, file_name)
    data: CVRowData = {"userId": user_id, "fileId": file_id, "fileName": file_name, "text": text}

    if existing is None:
        create_cv_row(data)
        return

    update_cv_row(existing.row_id, data)
    if existing.file_id:
        delete_cv_file(existing.file_id)
