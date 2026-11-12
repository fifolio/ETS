import pytest

from app.services.plans.validate_upgrade import validate_upgrade


@pytest.mark.parametrize(
    ("current", "target"),
    [("explore", "nextmove"), ("explore", "urgent"), ("nextmove", "urgent")],
)
def test_moving_up_is_allowed(current, target):
    assert validate_upgrade(current, target) is None


@pytest.mark.parametrize(
    ("current", "target", "message"),
    [
        ("nextmove", "nextmove", "already"),
        ("urgent", "nextmove", "above"),
        ("urgent", "explore", "free"),
        ("explore", "platinum", "Unknown"),
    ],
)
def test_everything_else_is_refused_with_a_reason(current, target, message):
    assert message in validate_upgrade(current, target)
