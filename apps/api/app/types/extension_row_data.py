from typing import TypedDict


class ExtensionRowData(TypedDict, total=False):
    userId: str
    installId: str
    browser: str
    browserVersion: str
    os: str
    extensionVersion: str
    lastUsedAt: str
    scanCount: int
    installedAt: str
