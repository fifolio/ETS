from pydantic import BaseModel


class LedgerRow(BaseModel):
    amount: int = 0
    kind: str = ""
    reason: str = ""
