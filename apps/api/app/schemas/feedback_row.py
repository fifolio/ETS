from pydantic import BaseModel


class FeedbackRow(BaseModel):
    """Shape of a row in the testimonials table, used by the Appwrite SDK for typed access."""

    userId: str
    quote: str | None = None
    internalSuggestions: str | None = None
    metricsSaved: str | None = None
    displayName: str | None = None
    role: str | None = None
    consent: bool = False
    status: str = "pending"
