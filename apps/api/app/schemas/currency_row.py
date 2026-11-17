from pydantic import BaseModel


class CurrencyRow(BaseModel):
    code: str
    name: str
    symbol: str
    rateFromUsd: float
