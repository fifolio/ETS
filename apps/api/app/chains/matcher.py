from langchain_groq import ChatGroq

from app.core.config import settings
from app.prompts.matcher import MATCHER_PROMPT
from app.schemas.verdict import MatchResult


def build_chain():
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set in the root .env file. "
            "Please set GROQ_API_KEY in your environment variables."
        )
    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
    )

    return MATCHER_PROMPT | llm.with_structured_output(MatchResult)


def analyze(cv_text: str, job_text: str) -> MatchResult:
    return build_chain().invoke({"cv": cv_text, "job": job_text})
