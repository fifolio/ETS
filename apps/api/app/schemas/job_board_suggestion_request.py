from pydantic import BaseModel, Field

from app.constants.suggestions import (
    MAX_COUNTRY_LENGTH,
    MAX_NAME_LENGTH,
    MAX_NOTES_LENGTH,
    MAX_URL_LENGTH,
)


class JobBoardSuggestionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=MAX_NAME_LENGTH, description="Name of the job board")
    url: str = Field(
        min_length=1,
        max_length=MAX_URL_LENGTH,
        description="Main address of its job section, for example https://www.indeed.com/jobs",
    )
    example_url: str | None = Field(
        default=None, max_length=MAX_URL_LENGTH, description="A link to one job post on that board"
    )
    country: str | None = Field(default=None, max_length=MAX_COUNTRY_LENGTH)
    notes: str | None = Field(default=None, max_length=MAX_NOTES_LENGTH)
