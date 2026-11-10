from pydantic import BaseModel, Field


class ExtensionReceipt(BaseModel):
    created: bool = Field(description="True for a new install, false for a known one")
