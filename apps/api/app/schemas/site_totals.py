from pydantic import BaseModel, Field


class SiteTotals(BaseModel):
    total_users: int = Field(description="Users who have scanned at least one job post")
    total_scans: int = Field(description="Job posts scanned by everyone")
    total_minutes_saved: float = Field(description="Reading time saved, in minutes")
    total_hours_saved: float = Field(description="Reading time saved, in hours")
    total_cash_saved_usd: float = Field(description="Cash equivalent of the time saved")
