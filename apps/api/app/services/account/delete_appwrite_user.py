from app.services.appwrite.get_users import get_users


def delete_appwrite_user(user_id: str) -> None:
    get_users().delete(user_id=user_id)
