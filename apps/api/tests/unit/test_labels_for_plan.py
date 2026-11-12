import pytest

from app.services.account.labels_for_plan import labels_for_plan


@pytest.mark.parametrize(
    ("current", "plan", "expected"),
    [
        (["cvdone"], "nextmove", ["cvdone", "nextmove"]),
        (["nextmove", "cvdone"], "urgent", ["cvdone", "urgent"]),
        (["urgent", "keepaccount"], "explore", ["keepaccount"]),
        ([], "explore", []),
    ],
)
def test_switches_the_plan_label_and_keeps_every_other_label(current, plan, expected):
    assert labels_for_plan(current, plan) == expected


def test_an_unknown_plan_is_refused():
    with pytest.raises(ValueError):
        labels_for_plan([], "platinum")
