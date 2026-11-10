import logging

from app.services.extensions.touch_extension import touch_extension

logger = logging.getLogger(__name__)


def record_extension_use(user_id: str, install_id: str | None, counted: bool) -> None:
    """Update the install's usage. Never raises: tracking must not break a scan."""
    if not install_id:
        return
    try:
        touch_extension(user_id, install_id, counted)
    except Exception:
        logger.exception("Could not update the extension's usage")
