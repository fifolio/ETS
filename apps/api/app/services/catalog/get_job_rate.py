from appwrite.query import Query

from app.core.config import settings
from app.schemas.job_row import JobRow
from app.services.appwrite.get_tables_db import get_tables_db


def get_job_rate(job_id: str) -> float | None:
    """The hourly rate of a job from the jobs table, or None if the job doesn't exist."""
    result = get_tables_db().list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_jobs_table_id,
        queries=[Query.equal("$id", job_id), Query.limit(1)],
        model_type=JobRow,
    )
    return result.rows[0].data.hourlyRateUsd if result.rows else None
