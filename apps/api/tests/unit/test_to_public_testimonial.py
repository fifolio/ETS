from app.schemas.feedback_row import FeedbackRow
from app.services.feedback.to_public_testimonial import to_public_testimonial

METRICS = '{"scans": 18, "words": 9000, "minutes_saved": 100.0}'


def make_row(**overrides):
    values = {
        "userId": "user-1",
        "quote": " Saved me hours. ",
        "internalSuggestions": "Add Safari support",
        "metricsSaved": METRICS,
        "displayName": "Jane D.",
        "role": "Nurse",
        "consent": True,
        "status": "approved",
    }
    return FeedbackRow(**{**values, **overrides})


def test_an_approved_row_becomes_a_public_testimonial():
    result = to_public_testimonial("row-1", make_row())

    assert result.model_dump() == {
        "id": "row-1",
        "quote": "Saved me hours.",
        "display_name": "Jane D.",
        "role": "Nurse",
        "hours_saved": 1.7,
        "scans": 18,
    }


def test_internal_suggestions_never_reach_the_public_version():
    result = to_public_testimonial("row-1", make_row())

    assert "internal" not in " ".join(result.model_dump()).lower()
    assert "Safari" not in result.model_dump_json()


def test_rows_that_are_not_approved_are_hidden():
    assert to_public_testimonial("row-1", make_row(status="pending")) is None
    assert to_public_testimonial("row-1", make_row(status="rejected")) is None


def test_rows_without_consent_or_without_a_quote_are_hidden():
    assert to_public_testimonial("row-1", make_row(consent=False)) is None
    assert to_public_testimonial("row-1", make_row(quote="   ")) is None
