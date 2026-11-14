from app.services.suggestions.find_covering_board import find_covering_board
from app.types.job_board import JobBoard

LINKEDIN = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore")


def test_an_address_under_a_supported_board_is_covered():
    assert find_covering_board("https://www.linkedin.com/jobs/search", [LINKEDIN]) == LINKEDIN


def test_a_broader_address_that_contains_a_supported_board_is_covered():
    assert find_covering_board("https://www.linkedin.com", [LINKEDIN]) == LINKEDIN


def test_www_and_case_are_ignored():
    assert find_covering_board("https://LinkedIn.com/jobs", [LINKEDIN]) == LINKEDIN


def test_a_different_website_is_not_covered():
    assert find_covering_board("https://wellfound.com/jobs", [LINKEDIN]) is None


def test_nothing_is_covered_when_there_are_no_boards():
    assert find_covering_board("https://www.linkedin.com/jobs", []) is None
