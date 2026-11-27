from app.constants.time_saved import AVG_JOB_POST_WORDS, MINUTES_SAVED_PER_SCAN, SECONDS_PER_WORD
from app.services.time_saved.get_time_saved_config import get_time_saved_config


def test_the_config_has_the_minutes_per_scan_and_the_credits_per_scan():
    assert get_time_saved_config().model_dump() == {"minutes_per_scan": 5.0, "credits_per_scan": 1}


def test_a_600_word_posting_at_half_a_second_per_word_is_5_minutes():
    assert (AVG_JOB_POST_WORDS, SECONDS_PER_WORD) == (600, 0.5)
    assert MINUTES_SAVED_PER_SCAN == 5.0
