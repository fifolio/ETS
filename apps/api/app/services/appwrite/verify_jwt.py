from appwrite.services.account import Account

from app.services.appwrite.new_client import new_client
from app.types.authenticated_user import AuthenticatedUser


def verify_jwt(token: str) -> AuthenticatedUser:
    """Return the user for a valid JWT. Raises AppwriteException if it's invalid."""
    client = new_client()  # deliberately no API key: this client acts as the user
    client.set_jwt(token)
    user = Account(client).get()
    return AuthenticatedUser(id=user.id, name=user.name, email=user.email)
