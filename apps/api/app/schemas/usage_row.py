from pydantic import BaseModel


class UsageRow(BaseModel):
    """Shape of a row in the usage_stats table, used by the Appwrite SDK for typed access."""

    scanCount: int = 0
    wordsTotal: int = 0
