import pytest

from app.services.feedback.build_display_name import build_display_name


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Firas Dabbabi", "Firas D."),
        ("Firas", "Firas"),
        ("Ana Maria Lopez", "Ana L."),
        ("  jane   doe ", "Jane D."),
        ("", "Anonymous"),
    ],
)
def test_the_public_name_is_a_first_name_and_an_initial(name, expected):
    assert build_display_name(name) == expected
