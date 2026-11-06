from appwrite.id import ID

from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.types.feedback_row_data import FeedbackRowData


def create_feedback_row(data: FeedbackRowData) -> None:
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_testimonials_table_id,
        row_id=ID.unique(),
        data=data,
    )
