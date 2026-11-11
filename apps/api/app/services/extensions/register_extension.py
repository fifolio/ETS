from datetime import UTC, datetime

from appwrite.exception import AppwriteException

from app.schemas.extension_registration import ExtensionRegistration
from app.services.extensions.create_extension import create_extension
from app.services.extensions.find_extension_id import find_extension_id
from app.services.extensions.update_extension import update_extension
from app.types.extension_row_data import ExtensionRowData


def register_extension(user_id: str, registration: ExtensionRegistration) -> bool:
    """Register a browser install for the user, or refresh it. Returns True when it is new."""
    details: ExtensionRowData = {
        "browser": registration.browser,
        "browserVersion": registration.browser_version,
        "os": registration.os,
        "extensionVersion": registration.extension_version,
        "lastUsedAt": datetime.now(UTC).isoformat(),
    }
    row_id = find_extension_id(user_id, registration.install_id)

    if row_id is None:
        try:
            create_extension(
                {
                    **details,
                    "userId": user_id,
                    "installId": registration.install_id,
                    "scanCount": 0,
                    "installedAt": details["lastUsedAt"],
                }
            )
            return True
        except AppwriteException as exc:
            if exc.code != 409:
                raise
            # Registered at the same moment by another request: refresh that row instead.
            row_id = find_extension_id(user_id, registration.install_id)
            if row_id is None:
                raise

    update_extension(row_id, details)
    return False
