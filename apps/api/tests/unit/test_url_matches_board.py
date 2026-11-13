import pytest

from app.services.job_boards.url_matches_board import url_matches_board

LINKEDIN = "https://www.linkedin.com/jobs"


@pytest.mark.parametrize(
    ("page", "board", "expected"),
    [
        ("https://www.linkedin.com/jobs/view/123", LINKEDIN, True),
        ("https://www.linkedin.com/jobs", LINKEDIN, True),
        ("https://www.linkedin.com/jobs/", LINKEDIN, True),
        ("https://linkedin.com/jobs/view/1", LINKEDIN, True),
        ("https://WWW.LinkedIn.com/Jobs/view/1", LINKEDIN, True),
        ("https://www.linkedin.com/jobs/collections/?currentJobId=1#top", LINKEDIN, True),
        ("https://www.linkedin.com/anything", "https://www.linkedin.com", True),
        ("https://www.linkedin.com/feed", LINKEDIN, False),
        ("https://www.linkedin.com/jobsearch/abc", LINKEDIN, False),
        ("https://www.linkedin.com/", LINKEDIN, False),
        ("https://uk.linkedin.com/jobs/view/1", LINKEDIN, False),
        ("https://www.example.com/jobs/1", LINKEDIN, False),
        ("https://evil.com/?u=https://www.linkedin.com/jobs", LINKEDIN, False),
        ("ftp://www.linkedin.com/jobs/1", LINKEDIN, False),
        ("not a url", LINKEDIN, False),
    ],
)
def test_a_page_matches_a_board_by_host_and_path(page, board, expected):
    assert url_matches_board(page, board) is expected
