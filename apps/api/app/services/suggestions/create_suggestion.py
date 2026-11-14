from appwrite.id import ID

from app.constants.suggestions import SUGGESTION_STATUS_PENDING
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.scans.hash_job_url import hash_job_url
from app.types.suggestion_row_data import SuggestionRowData
from app.types.validated_suggestion import ValidatedSuggestion


def create_suggestion(user_id: str, suggestion: ValidatedSuggestion) -> None:
    data: SuggestionRowData = {
        "userId": user_id,
        "name": suggestion.name,
        "url": suggestion.url,
        # Reuses the page-address hash: it ignores www., case, and a trailing slash.
        "urlHash": hash_job_url(suggestion.url),
        "exampleUrl": suggestion.example_url,
        "country": suggestion.country,
        "notes": suggestion.notes,
        "status": SUGGESTION_STATUS_PENDING,
    }
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_suggestions_table_id,
        row_id=ID.unique(),
        data=data,
    )
