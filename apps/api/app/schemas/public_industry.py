from pydantic import BaseModel


class PublicIndustry(BaseModel):
    id: str
    name: str
