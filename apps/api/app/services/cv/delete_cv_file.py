import logging

from appwrite.exception import AppwriteException

from app.core.config import settings
from app.services.appwrite.get_storage import get_storage

logger = logging.getLogger(__name__)


def delete_cv_file(file_id: str) -> None:
    """Best effort: a file that can't be deleted is logged, not raised."""
    try:
        get_storage().delete_file(settings.appwrite_cv_bucket_id, file_id)
    except AppwriteException:
        logger.warning("Could not delete the old CV file %s", file_id)
