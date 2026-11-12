from pydantic import BaseModel


class CheckoutResponse(BaseModel):
    checkout_url: str
