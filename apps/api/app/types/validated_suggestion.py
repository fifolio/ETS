from dataclasses import dataclass


@dataclass(frozen=True)
class ValidatedSuggestion:
    name: str
    url: str  # the cleaned main address
    example_url: str | None
    country: str | None
    notes: str | None
