from app.services.appwrite.get_users import get_users


def delete_account(user_id: str) -> None:
    get_users().delete(user_id=user_id)
