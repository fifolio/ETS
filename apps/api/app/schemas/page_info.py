from pydantic import BaseModel


class PageInfo(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
