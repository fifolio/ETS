from pydantic import BaseModel


class ManageUrlOut(BaseModel):
    url: str
