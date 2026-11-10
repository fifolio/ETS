from pydantic import BaseModel


class ScanRow(BaseModel):
    resultJson: str | None = None
