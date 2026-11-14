import app.services.suggestions.create_suggestion as module
from app.services.scans.hash_job_url import hash_job_url
from app.types.validated_suggestion import ValidatedSuggestion


class FakeTables:
    def __init__(self):
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)


def test_stores_the_suggestion_as_pending_with_a_hash_of_the_address(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)
    suggestion = ValidatedSuggestion(
        "Indeed", "https://www.indeed.com/jobs", "https://www.indeed.com/viewjob?jk=1", "USA", "Big"
    )

    module.create_suggestion("user-1", suggestion)

    data = tables.calls[0]["data"]
    assert data["status"] == "pending" and data["userId"] == "user-1"
    assert data["urlHash"] == hash_job_url("https://www.indeed.com/jobs")
    assert (data["name"], data["exampleUrl"], data["country"], data["notes"]) == (
        "Indeed",
        "https://www.indeed.com/viewjob?jk=1",
        "USA",
        "Big",
    )


def test_optional_fields_that_are_missing_are_stored_as_none(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)

    module.create_suggestion(
        "user-1", ValidatedSuggestion("Indeed", "https://www.indeed.com/jobs", None, None, None)
    )

    data = tables.calls[0]["data"]
    assert (data["exampleUrl"], data["country"], data["notes"]) == (None, None, None)
