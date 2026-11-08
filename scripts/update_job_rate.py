
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from appwrite.query import Query

from app.core.config import settings 
from app.schemas.job_row import JobRow 
from app.services.appwrite.get_tables_db import get_tables_db  


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(
            'Usage: update_job_rate.py <industry-slug> '
            '"<job name>" <hourly-rate-usd>'
        )

    industry, job_name, rate_arg = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        rate = float(rate_arg)
    except ValueError:
        sys.exit("Error: hourly rate must be a valid number.")

    if rate < 0:
        sys.exit("Error: hourly rate cannot be negative.")

    tables = get_tables_db()

    found = tables.list_rows(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_jobs_table_id,
        queries=[
            Query.equal("industryId", industry),
            Query.equal("name", job_name),
            Query.limit(1),
        ],
        model_type=JobRow,
    )

    if not found.rows:
        sys.exit(f'No job "{job_name}" in industry "{industry}".')

    tables.update_row(
        database_id=settings.appwrite_database_id,
        table_id=settings.appwrite_jobs_table_id,
        row_id=found.rows[0].id,
        data={"hourlyRateUsd": rate},
    )

    print(
        f'Updated "{job_name}" in "{industry}" '
        f'to ${rate:.2f} per hour.'
    )


if __name__ == "__main__":
    main()
