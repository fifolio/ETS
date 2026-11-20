from pydantic import BaseModel


class CurrencyOut(BaseModel):
    code: str
    name: str
    symbol: str
    rate_from_usd: float
