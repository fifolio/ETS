import pytest

from app.services.suggestions.normalize_board_url import normalize_board_url


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.indeed.com/jobs?q=dev#top", "https://www.indeed.com/jobs"),
        ("HTTPS://Wellfound.COM/jobs/", "https://wellfound.com/jobs"),
        ("http://example.com", "http://example.com"),
        ("https://example.com:443/careers", "https://example.com/careers"),
        ("  https://example.com/jobs  ", "https://example.com/jobs"),
        ("ftp://example.com/jobs", None),
        ("example.com/jobs", None),
        ("https://user:pass@example.com/jobs", None),
        ("https://example.com:8080/jobs", None),
        ("https://localhost/jobs", None),
        ("https://intranet/jobs", None),
        ("https://printer.local/jobs", None),
        ("http://192.168.1.10/jobs", None),
        ("http://[::1]/jobs", None),
        ("", None),
        ("not a url", None),
    ],
)
def test_keeps_only_a_clean_public_web_address(url, expected):
    assert normalize_board_url(url) == expected
