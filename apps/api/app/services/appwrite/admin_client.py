from appwrite.client import Client

from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.services.appwrite.new_client import new_client


def admin_client() -> Client:
    if not settings.appwrite_api_key:
        raise ConfigurationError("APPWRITE_API_KEY must be set in .env")
    client = new_client()
    client.set_key(settings.appwrite_api_key)
    return client
