from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def increment_usage(user_id: str, words: int) -> None:
    """Add one scan and `words` words to the user's totals. Each step is atomic on the server."""
    tables = get_tables_db()
    for column, value in (("scanCount", 1), ("wordsTotal", words)):
        if value:
            tables.increment_row_column(
                database_id=settings.appwrite_database_id,
                table_id=settings.appwrite_usage_table_id,
                row_id=user_id,
                column=column,
                value=value,
            )
