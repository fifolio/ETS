from app.services.account.delete_appwrite_user import delete_appwrite_user
from app.services.account.delete_user_data import delete_user_data


def delete_user_account(user_id: str) -> None:
    """Delete the user's data first, so a failure leaves the account in place to retry."""
    delete_user_data(user_id)
    delete_appwrite_user(user_id)
