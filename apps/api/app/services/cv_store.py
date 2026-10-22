import logging
from dataclasses import dataclass

from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.input_file import InputFile
from appwrite.query import Query
from pydantic import BaseModel

from app.core.config import settings
from app.services.appwrite_client import storage, tables_db

logger = logging.getLogger(__name__)


class CVRow(BaseModel):
    """Shape of a row in the cvs table, used by the Appwrite SDK for typed access."""

    userId: str
    fileId: str | None = None
    fileName: str | None = None
    text: str


@dataclass
class StoredCV:
    row_id: str
    file_id: str | None
    file_name: str | None
    text: str


def get_cv(user_id: str) -> StoredCV | None:
    result = tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_cvs_table_id,
        queries=[Query.equal("userId", user_id), Query.limit(1)],
        model_type=CVRow,
    )
    if not result.rows:
        return None
    row = result.rows[0]
    return StoredCV(
        row_id=row.id,
        file_id=row.data.fileId,
        file_name=row.data.fileName,
        text=row.data.text,
    )


def save_cv(user_id: str, file_name: str, pdf_bytes: bytes, text: str) -> None:
    """Store the PDF and its text. Replaces the user's previous CV if there is one."""
    existing = get_cv(user_id)
    uploaded = storage().create_file(
        settings.appwrite_cv_bucket_id,
        ID.unique(),
        InputFile.from_bytes(pdf_bytes, file_name),
    )
    data = {"userId": user_id, "fileId": uploaded.id, "fileName": file_name, "text": text}

    if existing is None:
        tables_db().create_row(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_cvs_table_id,
            row_id=ID.unique(),
            data=data,
        )
        return

    tables_db().update_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_cvs_table_id,
        row_id=existing.row_id,
        data=data,
    )
    if existing.file_id:
        try:
            storage().delete_file(settings.appwrite_cv_bucket_id, existing.file_id)
        except AppwriteException:
            logger.warning("Could not delete the old CV file %s", existing.file_id)
