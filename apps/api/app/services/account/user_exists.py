from appwrite.exception import AppwriteException

from app.services.appwrite.get_users import get_users


def user_exists(user_id: str) -> bool:
    try:
        get_users().get(user_id=user_id)
    except AppwriteException as exc:
        if exc.code == 404:
            return False
        raise
    return True
