from pydantic import BaseModel, Field


class TimeSavedConfigOut(BaseModel):
    minutes_per_scan: float = Field(description="Average reading time one scan saves")
    credits_per_scan: int = Field(description="Credits one scan costs")
