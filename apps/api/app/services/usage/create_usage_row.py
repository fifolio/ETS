from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def create_usage_row(user_id: str, words: int) -> None:
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_usage_table_id,
        row_id=user_id,
        data={"scanCount": 1, "wordsTotal": words},
    )
