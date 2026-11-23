from app.services.topups.get_topup_config import get_topup_config


def test_the_config_describes_the_range_the_step_and_the_rate():
    assert get_topup_config().model_dump() == {
        "min_usd": 3.0,
        "max_usd": 50.0,
        "step_usd": 0.25,
        "credits_per_step": 2,
        "credits_per_usd": 8,
    }
