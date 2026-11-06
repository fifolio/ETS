from pydantic import BaseModel


class FeedbackReceipt(BaseModel):
    status: str
