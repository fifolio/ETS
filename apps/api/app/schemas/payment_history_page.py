from app.schemas.page_info import PageInfo
from app.schemas.payment_entry_out import PaymentEntryOut


class PaymentHistoryPage(PageInfo):
    items: list[PaymentEntryOut]
