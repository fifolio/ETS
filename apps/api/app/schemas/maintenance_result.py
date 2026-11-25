from pydantic import BaseModel, Field


class MaintenanceResult(BaseModel):
    explore_renewals_due: int = Field(description="Explore accounts whose monthly credits are due")
    expired_due: int = Field(description="Paid plans past their period end plus the grace days")
    reminders_due: int = Field(
        description="Plans ending or renewing within a day, not yet reminded"
    )
    explore_renewed: int = Field(description="Actually renewed (0 in a dry run)")
    ended: int = Field(description="Actually ended (0 in a dry run)")
    reminded: int = Field(description="Actually reminded (0 in a dry run)")
    failed: int = Field(description="Number of failed operations")
    dry_run: bool = Field(description="Whether this is a dry run")
