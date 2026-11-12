from app.services.plans.list_public_plans import list_public_plans


def test_lists_the_three_plans_from_lowest_to_highest():
    plans = list_public_plans()

    assert [plan.id for plan in plans] == ["explore", "nextmove", "urgent"]
    assert [plan.name for plan in plans] == ["Explore", "Next Move", "Urgent"]


def test_the_job_board_limits_grow_and_urgent_has_no_limit():
    limits = {plan.id: plan.max_job_boards for plan in list_public_plans()}

    assert limits == {"explore": 1, "nextmove": 3, "urgent": None}
