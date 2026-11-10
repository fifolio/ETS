from datetime import UTC, datetime

from app.services.extensions.find_extension_id import find_extension_id
from app.services.extensions.increment_extension_scans import increment_extension_scans
from app.services.extensions.update_extension import update_extension


def touch_extension(user_id: str, install_id: str, counted: bool) -> None:
    """Record that an install was just used, and count the scan when `counted` is true."""
    row_id = find_extension_id(user_id, install_id)
    if row_id is None:
        return  # an install that never registered: nothing to update
    update_extension(row_id, {"lastUsedAt": datetime.now(UTC).isoformat()})
    if counted:
        increment_extension_scans(row_id)
