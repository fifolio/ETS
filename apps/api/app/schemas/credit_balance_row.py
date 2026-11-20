from pydantic import BaseModel


class CreditBalanceRow(BaseModel):
    subscriptionCredits: int = 0
    promotionalCredits: int = 0
    purchasedCredits: int = 0
