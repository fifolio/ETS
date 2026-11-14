from pydantic import BaseModel, Field


class SuggestionReceipt(BaseModel):
    status: str
    remaining_today: int = Field(description="How many more suggestions the user can send today")
