from appwrite.services.account import Account

from app.services.account.read_subscription import read_subscription
from app.services.appwrite.new_client import new_client
from app.services.appwrite.read_user_prefs import read_user_prefs
from app.types.authenticated_user import AuthenticatedUser


def verify_jwt(token: str) -> AuthenticatedUser:
    """Return the user for a valid JWT. Raises AppwriteException if it's invalid."""
    client = new_client()  # deliberately no API key: this client acts as the user
    client.set_jwt(token)
    user = Account(client).get()
    return AuthenticatedUser(
        id=user.id,
        name=user.name,
        email=user.email,
        email_verified=user.emailverification,
        prefs=read_user_prefs(user.prefs),
        labels=list(user.labels),
        subscription=read_subscription(list(user.labels)),
    )
