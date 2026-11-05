from pydantic import BaseModel, Field


class CleanupResult(BaseModel):
    checked: int = Field(description="Accounts looked at")
    expired: int = Field(description="Accounts that missed the setup deadline")
    deleted: int = Field(description="Accounts actually deleted (0 in a dry run)")
    dry_run: bool = Field(description="Whether this is a dry run (no actual deletions)")
