from app.core.config import settings
from app.schemas.cv_row import CVRow
from app.schemas.extension_row import ExtensionRow
from app.schemas.usage_row import UsageRow
from app.services.appwrite.iter_table_rows import iter_table_rows


def find_data_owner_ids() -> set[str]:
    """IDs of users with a stored CV, usage totals, or extension installs."""
    owners = {row.data.userId for row in iter_table_rows(settings.appwrite_cvs_table_id, CVRow)}
    owners.update(row.id for row in iter_table_rows(settings.appwrite_usage_table_id, UsageRow))
    owners.update(
        row.data.userId
        for row in iter_table_rows(settings.appwrite_extensions_table_id, ExtensionRow)
    )
    return owners
