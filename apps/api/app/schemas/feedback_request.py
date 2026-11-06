from pydantic import BaseModel, Field, model_validator

from app.constants.feedback import MAX_QUOTE_LENGTH, MAX_SUGGESTIONS_LENGTH


class FeedbackRequest(BaseModel):
    quote: str = Field(default="", max_length=MAX_QUOTE_LENGTH, description="Public testimonial")
    internal_suggestions: str = Field(
        default="", max_length=MAX_SUGGESTIONS_LENGTH, description="Private suggestions"
    )
    consent: bool = Field(
        default=False, description="Agrees to show the quote, first name, and role publicly"
    )

    @model_validator(mode="after")
    def check_content(self):
        quote = self.quote.strip()
        if not quote and not self.internal_suggestions.strip():
            raise ValueError("Write a testimonial, a suggestion, or both.")
        if quote and not self.consent:
            raise ValueError("Consent is required to publish a testimonial.")
        return self
