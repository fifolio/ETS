from appwrite.query import Query

from app.core.config import settings
from app.schemas.job_row import JobRow
from app.schemas.public_job import PublicJob
from app.services.appwrite.iter_table_rows import iter_table_rows


def list_industry_jobs(industry_id: str) -> list[PublicJob]:
    rows = iter_table_rows(
        settings.appwrite_jobs_table_id, JobRow, [Query.equal("industryId", industry_id)]
    )
    jobs = [
        PublicJob(id=row.id, name=row.data.name, hourly_rate_usd=row.data.hourlyRateUsd)
        for row in rows
    ]
    return sorted(jobs, key=lambda job: job.name.lower())
