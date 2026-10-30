from pydantic import BaseModel, Field


class CVInfo(BaseModel):
    file_name: str | None = Field(default=None, description="Original file name")
    characters: int = Field(description="Characters of text extracted from the CV")
