from pydantic import BaseModel


class IndustryRow(BaseModel):
    """Shape of a row in the industries table. The row ID is the industry's slug."""

    name: str
