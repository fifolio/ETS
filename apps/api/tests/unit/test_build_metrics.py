from app.services.feedback.build_metrics import build_metrics
from app.types.usage_stats import UsageStats


def test_converts_words_to_minutes():
    metrics = build_metrics(UsageStats(scans=3, words=1800))

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (3, 1800, 8.0)


def test_a_900_word_job_post_saves_four_minutes():
    assert build_metrics(UsageStats(scans=1, words=900)).minutes_saved == 4.0


def test_no_usage_means_zero_everything():
    metrics = build_metrics(UsageStats(scans=0, words=0))

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (0, 0, 0.0)


def test_totals_far_beyond_the_old_limit_still_add_up():
    metrics = build_metrics(UsageStats(scans=10_000, words=7_000_000))

    assert (metrics.scans, metrics.minutes_saved) == (10_000, 31111.1)
