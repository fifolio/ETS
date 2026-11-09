from appwrite.exception import AppwriteException

from app.services.usage.create_usage_row import create_usage_row
from app.services.usage.increment_usage import increment_usage
from app.types.scan_savings import ScanSavings


def record_scan_usage(user_id: str, words: int, savings: ScanSavings) -> None:
    """Count one scan of `words` words for the user, creating their row on the first scan."""
    try:
        increment_usage(user_id, words, savings)
    except AppwriteException as exc:
        if exc.code != 404:
            raise
        try:
            create_usage_row(user_id, words, savings)
        except AppwriteException as create_exc:
            if create_exc.code != 409:
                raise
            increment_usage(user_id, words, savings)  # another request created the row first
