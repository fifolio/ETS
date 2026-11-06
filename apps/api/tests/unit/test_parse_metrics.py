import pytest

from app.services.feedback.parse_metrics import parse_metrics


def test_reads_stored_metrics():
    metrics = parse_metrics('{"scans": 18, "words": 9000, "minutes_saved": 40.0}')

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (18, 9000, 40.0)


@pytest.mark.parametrize("text", [None, "", "not json", "[]", '{"scans": 1}'])
def test_anything_unreadable_becomes_zeros(text):
    metrics = parse_metrics(text)

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (0, 0, 0.0)
