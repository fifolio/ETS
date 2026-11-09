from pydantic import BaseModel


class JobRow(BaseModel):
    """Shape of a row in the jobs table, used by the Appwrite SDK for typed access."""

    name: str
    industryId: str
    hourlyRateUsd: float
