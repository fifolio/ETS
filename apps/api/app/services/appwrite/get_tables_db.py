from appwrite.services.tables_db import TablesDB

from app.services.appwrite.admin_client import admin_client


def get_tables_db() -> TablesDB:
    return TablesDB(admin_client())
