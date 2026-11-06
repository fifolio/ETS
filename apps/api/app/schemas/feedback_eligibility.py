from pydantic import BaseModel, Field


class FeedbackEligibility(BaseModel):
    eligible: bool = Field(description="True when all three conditions are met")
    trial_over: bool = Field(description="Enough days have passed since sign-up")
    enough_scans: bool = Field(description="The user made enough scans")
    already_submitted: bool = Field(description="The user already sent feedback")
