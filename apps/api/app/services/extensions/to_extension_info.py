from app.schemas.extension_info import ExtensionInfo
from app.schemas.extension_row import ExtensionRow


def to_extension_info(row_id: str, row: ExtensionRow) -> ExtensionInfo:
    return ExtensionInfo(
        id=row_id,
        browser=row.browser,
        browser_version=row.browserVersion,
        os=row.os,
        extension_version=row.extensionVersion,
        installed_at=row.installedAt,
        last_used_at=row.lastUsedAt,
        scan_count=row.scanCount,
    )
