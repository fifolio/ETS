import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import settings
from app.services.appwrite_client import storage, tables_db

def main():
    db = settings.appwrite_database_id
    tables_db().list_rows(database_id=db, table_id=settings.appwrite_cvs_table_id)
    print("cvs table: OK")
    tables_db().list_rows(database_id=db, table_id=settings.appwrite_scans_table_id)
    print("scans table: OK")
    storage().list_files(settings.appwrite_cv_bucket_id)
    print("cvs bucket: OK")

if __name__ == "__main__":
    main()