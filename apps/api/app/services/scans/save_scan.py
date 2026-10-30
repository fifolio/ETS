from appwrite.id import ID

from app.core.config import settings
from app.schemas.match_result import MatchResult
from app.services.appwrite.get_tables_db import get_tables_db


def save_scan(
    user_id: str, result: MatchResult, job_url: str | None, job_title: str | None
) -> None:
    get_tables_db().create_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_scans_table_id,
        row_id=ID.unique(),
        data={
            "userId": user_id,
            "jobUrl": job_url,
            "jobTitle": job_title,
            "verdict": result.verdict.value,
            "score": result.score,
            "resultJson": result.model_dump_json(),
        },
    )
