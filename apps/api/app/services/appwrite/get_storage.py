from appwrite.services.storage import Storage

from app.services.appwrite.admin_client import admin_client


def get_storage() -> Storage:
    return Storage(admin_client())
