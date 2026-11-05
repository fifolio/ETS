import pytest

from app.services.profile.missing_profile_fields import missing_profile_fields

ALL_FIELDS = [
    "role",
    "seniority",
    "yearsOfExperience",
    "currentLocation",
    "desiredLocations",
    "workArrangements",
    "employmentTypes",
]


def test_a_complete_profile_has_nothing_missing(complete_prefs):
    assert missing_profile_fields(complete_prefs) == []


def test_an_empty_profile_is_missing_everything():
    assert missing_profile_fields({}) == ALL_FIELDS


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seniority", "wizard"),
        ("yearsOfExperience", -1),
        ("yearsOfExperience", 61),
        ("yearsOfExperience", True),
        ("workArrangements", ["teleport"]),
        ("desiredLocations", ["  "]),
    ],
)
def test_invalid_values_count_as_missing(complete_prefs, field, value):
    assert missing_profile_fields({**complete_prefs, field: value}) == [field]
