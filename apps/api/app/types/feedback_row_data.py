from typing import TypedDict


class FeedbackRowData(TypedDict):
    userId: str
    quote: str
    internalSuggestions: str
    metricsSaved: str
    displayName: str
    role: str
    consent: bool
    status: str
