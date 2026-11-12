from app.services.plans.find_plan import find_plan


def test_finds_a_plan_by_its_id():
    plan = find_plan("nextmove")

    assert (plan.name, plan.max_job_boards) == ("Next Move", 3)


def test_an_unknown_plan_is_none():
    assert find_plan("platinum") is None
