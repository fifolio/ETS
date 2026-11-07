from pydantic import BaseModel


class CVRow(BaseModel):
    """Shape of a row in the cvs table, used by the Appwrite SDK for typed access."""

    userId: str
    fileName: str | None = None
    text: str
