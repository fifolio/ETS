from typing import Literal

CreditKindFilter = Literal["all", "subscription", "promotional", "purchased"]
CreditChangeFilter = Literal["all", "added", "used"]
PaymentStatusFilter = Literal["all", "completed", "failed", "underpaid", "refunded"]
PaymentProductFilter = Literal["all", "plan", "topup"]
