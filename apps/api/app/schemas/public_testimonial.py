from pydantic import BaseModel


class PublicTestimonial(BaseModel):
    id: str
    quote: str
    display_name: str
    role: str | None
    hours_saved: float
    scans: int
