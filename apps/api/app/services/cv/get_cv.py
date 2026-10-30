from appwrite.query import Query

from app.core.config import settings
from app.schemas.cv_row import CVRow
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.stored_cv import StoredCV


def get_cv(user_id: str) -> StoredCV | None:
    result = get_tables_db().list_rows(
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
