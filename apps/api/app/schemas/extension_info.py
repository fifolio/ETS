from pydantic import BaseModel


class ExtensionInfo(BaseModel):
    id: str
    browser: str | None
    browser_version: str | None
    os: str | None
    extension_version: str | None
    installed_at: str | None
    last_used_at: str | None
    scan_count: int
