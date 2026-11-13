from pydantic import BaseModel


class JobBoardRow(BaseModel):
    """Shape of a row in the job_boards table. The row ID is the board's slug."""

    name: str
    url: str
    minPlan: str | None = None
    isActive: bool = True
