from typing import TypedDict


class SuggestionRowData(TypedDict):
    userId: str
    name: str
    url: str
    urlHash: str
    exampleUrl: str | None
    country: str | None
    notes: str | None
    status: str
