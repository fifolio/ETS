from pydantic import BaseModel


class SuggestionRow(BaseModel):
    """Shape of a row in the job_board_suggestions table (only what we read back)."""

    userId: str
