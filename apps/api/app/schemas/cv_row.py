from pydantic import BaseModel


class CVRow(BaseModel):
    """Shape of a row in the cvs table, used by the Appwrite SDK for typed access."""

    userId: str
    fileId: str | None = None
    fileName: str | None = None
    text: str
