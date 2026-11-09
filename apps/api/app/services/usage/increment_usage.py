from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.scan_savings import ScanSavings


def increment_usage(user_id: str, words: int, savings: ScanSavings) -> None:
    """Add one scan and its words, minutes, and cash to the user's totals (atomic per column)."""
    tables = get_tables_db()
    amounts = (
        ("scanCount", 1),
        ("wordsTotal", words),
        ("minutesTotal", savings.minutes),
        ("cashTotal", savings.cash),
    )
    for column, value in amounts:
        if value:
            tables.increment_row_column(
                database_id=settings.appwrite_database_id,
                table_id=settings.appwrite_usage_table_id,
                row_id=user_id,
                column=column,
                value=value,
            )
