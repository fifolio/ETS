import pytest

from app.services.job_boards.normalize_min_plan import normalize_min_plan


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("explore", "explore"),
        ("nextmove", "nextmove"),
        ("urgent", "urgent"),
        ("platinum", "urgent"),
        ("", "urgent"),
        (None, "urgent"),
    ],
)
def test_a_missing_or_unknown_tier_means_the_highest_tier(value, expected):
    assert normalize_min_plan(value) == expected
