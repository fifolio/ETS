import pytest

from app.services.account.read_subscription import read_subscription


@pytest.mark.parametrize(
    ("labels", "expected"),
    [
        ([], "explore"),
        (["nextmove"], "nextmove"),
        (["nextmove", "urgent"], "urgent"),
        (["admin", "cvdone"], "explore"),
    ],
)
def test_the_plan_is_the_highest_plan_label(labels, expected):
    assert read_subscription(labels) == expected
