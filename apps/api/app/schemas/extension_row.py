from pydantic import BaseModel


class ExtensionRow(BaseModel):
    """Shape of a row in the extensions table, used by the Appwrite SDK for typed access."""

    userId: str
    installId: str = ""
    browser: str | None = None
    browserVersion: str | None = None
    os: str | None = None
    extensionVersion: str | None = None
    installedAt: str | None = None
    lastUsedAt: str | None = None
    scanCount: int = 0
