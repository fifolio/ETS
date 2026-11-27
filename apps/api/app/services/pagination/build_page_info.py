import math

from app.schemas.page_info import PageInfo


def build_page_info(page: int, page_size: int, total: int) -> PageInfo:
    """There is always at least one page, even when the list is empty."""
    return PageInfo(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=max(1, math.ceil(total / page_size)),
    )
