import logging
from typing import Any

logger = logging.getLogger(__name__)


def send_notification(user_id: str, kind: str, details: dict[str, Any]) -> None:
    """Sends a notification to the user with the given ID, kind, and details."""
    logger.info("Notification %s for user %s: %s", kind, user_id, details)
