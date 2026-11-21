from app.core.config import settings
from app.services.appwrite.delete_row_by_id import delete_row_by_id
from app.services.appwrite.delete_rows_by_user import delete_rows_by_user
from app.services.cv.delete_cv import delete_cv
from app.services.usage.delete_usage_row import delete_usage_row


def delete_user_data(user_id: str) -> None:
    """Delete what the user left behind: CV, usage, credits, subscription, scans, and more.

    Testimonials and payment records are kept on purpose.
    """
    delete_cv(user_id)
    delete_usage_row(user_id)
    delete_row_by_id(settings.appwrite_credit_balances_table_id, user_id)
    delete_row_by_id(settings.appwrite_subscriptions_table_id, user_id)
    delete_rows_by_user(settings.appwrite_credit_ledger_table_id, user_id)
    delete_rows_by_user(settings.appwrite_scans_table_id, user_id)
    delete_rows_by_user(settings.appwrite_extensions_table_id, user_id)
    delete_rows_by_user(settings.appwrite_suggestions_table_id, user_id)
