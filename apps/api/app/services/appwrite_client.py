from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.storage import Storage
from appwrite.services.tables_db import TablesDB

from app.core.config import settings
from app.core.errors import ConfigurationError


def _new_client() -> Client:
    if not (settings.appwrite_endpoint and settings.appwrite_project_id):
        raise ConfigurationError("APPWRITE_ENDPOINT and APPWRITE_PROJECT_ID must be set in .env")

    client = Client()
    client.set_endpoint(settings.appwrite_endpoint)
    client.set_project(settings.appwrite_project_id)
    return client


def _admin_client() -> Client:
    if not settings.appwrite_api_key:
        raise ConfigurationError("APPWRITE_API_KEY must be set in .env")

    client = _new_client()
    client.set_key(settings.appwrite_api_key)
    return client


def tables_db() -> TablesDB:
    return TablesDB(_admin_client())


def storage() -> Storage:
    return Storage(_admin_client())


def verify_jwt(token: str) -> str:
    """Return the user ID for a valid user JWT. Raises AppwriteException if it's invalid."""
    client = _new_client()
    client.set_jwt(token)
    return Account(client).get().id
