from pydantic import BaseModel, Field


class CleanupResult(BaseModel):
    checked: int = Field(description="Accounts looked at")
    expired: int = Field(description="Accounts that missed the setup deadline")
    deleted: int = Field(description="Expired accounts actually deleted (0 in a dry run)")
    orphaned: int = Field(
        default=0, description="Users whose data remains after their account was deleted"
    )
    orphans_cleaned: int = Field(
        default=0, description="Leftover data sets actually deleted (0 in a dry run)"
    )
    failed: int = Field(default=0, description="Deletions that failed and will be retried next run")
    dry_run: bool = Field(description="Whether this was a dry run (no deletions performed)")
