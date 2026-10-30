from langchain_groq import ChatGroq

from app.core.config import settings
from app.prompts.matcher import MATCHER_PROMPT
from app.schemas.match_result import MatchResult


def build_chain(model: str):
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not set in the root .env file")
    llm = ChatGroq(model=model, api_key=settings.groq_api_key, temperature=0)
    return MATCHER_PROMPT | llm.with_structured_output(MatchResult)
