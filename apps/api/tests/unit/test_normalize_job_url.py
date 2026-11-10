import pytest

from app.services.scans.normalize_job_url import normalize_job_url


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com/jobs/123", "https://example.com/jobs/123"),
        ("https://example.com/jobs/123?utm_source=x&utm_medium=y", "https://example.com/jobs/123"),
        ("https://example.com/jobs/123?fbclid=abc&id=5", "https://example.com/jobs/123?id=5"),
        ("https://example.com/jobs/123#apply", "https://example.com/jobs/123"),
        ("HTTPS://WWW.Example.com/jobs/123/", "https://example.com/jobs/123"),
        ("https://example.com/jobs?b=2&a=1", "https://example.com/jobs?a=1&b=2"),
        (
            "https://www.linkedin.com/jobs/collections/?currentJobId=3912345678&trk=abc",
            "https://linkedin.com/jobs/collections?currentJobId=3912345678",
        ),
        ("https://example.com:443/jobs/1", "https://example.com/jobs/1"),
        ("https://example.com:8080/jobs/1", "https://example.com:8080/jobs/1"),
        ("https://example.com/Jobs/ABC", "https://example.com/Jobs/ABC"),
        ("  Not A URL  ", "not a url"),
    ],
)
def test_normalizes_the_url(url, expected):
    assert normalize_job_url(url) == expected
