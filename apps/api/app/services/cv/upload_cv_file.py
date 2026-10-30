from appwrite.id import ID
from appwrite.input_file import InputFile

from app.core.config import settings
from app.services.appwrite.get_storage import get_storage


def upload_cv_file(pdf_bytes: bytes, file_name: str) -> str:
    """Store the PDF and return its file ID."""
    uploaded = get_storage().create_file(
        settings.appwrite_cv_bucket_id,
        ID.unique(),
        InputFile.from_bytes(pdf_bytes, file_name),
    )
    return uploaded.id
