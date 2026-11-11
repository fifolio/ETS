from appwrite.query import Query

from app.core.config import settings
from app.schemas.extension_info import ExtensionInfo
from app.schemas.extension_row import ExtensionRow
from app.services.appwrite.iter_table_rows import iter_table_rows
from app.services.extensions.to_extension_info import to_extension_info


def list_user_extensions(user_id: str) -> list[ExtensionInfo]:
    """The user's installs, the most recently used first."""
    rows = iter_table_rows(
        settings.appwrite_extensions_table_id, ExtensionRow, [Query.equal("userId", user_id)]
    )
    items = [to_extension_info(row.id, row.data) for row in rows]
    return sorted(items, key=lambda item: item.last_used_at or "", reverse=True)
