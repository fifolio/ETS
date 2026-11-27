from app.schemas.credit_entry_out import CreditEntryOut
from app.schemas.page_info import PageInfo


class CreditHistoryPage(PageInfo):
    items: list[CreditEntryOut]
