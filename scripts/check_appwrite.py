import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import settings  # noqa: E402
from app.services.appwrite.get_tables_db import get_tables_db  # noqa: E402


def main():
    tables = get_tables_db()
    checks = {
        "cvs": settings.appwrite_cvs_table_id,
        "scans": settings.appwrite_scans_table_id,
        "usage_stats": settings.appwrite_usage_table_id,
        "testimonials": settings.appwrite_testimonials_table_id,
        "industries": settings.appwrite_industries_table_id,
        "jobs": settings.appwrite_jobs_table_id,
        "extensions": settings.appwrite_extensions_table_id,
        "job_boards": settings.appwrite_job_boards_table_id,

    }
    for name, table_id in checks.items():
        tables.list_rows(database_id=settings.appwrite_database_id, table_id=table_id)
        print(f"{name} table: OK")


if __name__ == "__main__":
    main()