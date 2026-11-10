from pydantic import BaseModel


class ExtensionRow(BaseModel):
    """Shape of a row in the extensions table, used by the Appwrite SDK for typed access."""

    userId: str
    installId: str = ""
    scanCount: int = 0
