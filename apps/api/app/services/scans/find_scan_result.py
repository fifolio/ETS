import logging

from appwrite.query import Query

from app.core.config import settings
from app.schemas.match_result import MatchResult
from app.schemas.scan_row import ScanRow
from app.services.appwrite.get_tables_db import get_tables_db

logger = logging.getLogger(__name__)


def find_scan_result(user_id: str, url_hash: str) -> MatchResult | None:
    """The stored result of the scan with this URL hash for this user, if there is one."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_scans_table_id,
        queries=[
            Query.equal("userId", user_id),
            Query.equal("urlHash", url_hash),
            Query.limit(1),
        ],
        model_type=ScanRow,
    )
    stored = result.rows[0].data.resultJson if result.rows else None
    if not stored:
        return None
    try:
        return MatchResult.model_validate_json(stored)
    except ValueError:
        logger.warning("The stored result of a previous scan could not be read")
        return None
