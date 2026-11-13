from pydantic import BaseModel, Field


class JobBoardOut(BaseModel):
    id: str
    name: str
    url: str
    plan: str = Field(description="The lowest plan that includes this board")
    plan_name: str = Field(description="That plan's display name")
