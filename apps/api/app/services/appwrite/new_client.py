from appwrite.client import Client

from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError


def new_client() -> Client:
    if not (settings.appwrite_endpoint and settings.appwrite_project_id):
        raise ConfigurationError("APPWRITE_ENDPOINT and APPWRITE_PROJECT_ID must be set in .env")
    client = Client()
    client.set_endpoint(settings.appwrite_endpoint)
    client.set_project(settings.appwrite_project_id)
    return client
