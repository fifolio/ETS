import pytest

from app.services.pagination.build_page_info import build_page_info


@pytest.mark.parametrize(("total", "pages"), [(0, 1), (1, 1), (10, 1), (11, 2), (25, 3)])
def test_the_pages_are_the_total_over_the_page_size_rounded_up_and_at_least_one(total, pages):
    assert build_page_info(1, 10, total).total_pages == pages


def test_keeps_the_page_the_page_size_and_the_total():
    info = build_page_info(3, 10, 25)

    assert (info.page, info.page_size, info.total) == (3, 10, 25)
