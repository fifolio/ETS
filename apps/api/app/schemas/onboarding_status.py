from pydantic import BaseModel, Field


class OnboardingStatus(BaseModel):
    steps: dict[str, bool] = Field(description="Each setup step and whether it is done")
    next_step: str | None = Field(description="First step not done, or null when finished")
    complete: bool = Field(description="True when every step is done")
    missing_profile_fields: list[str] = Field(description="Profile answers still missing")
