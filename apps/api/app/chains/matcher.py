import logging

import groq
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq

from app.core.config import settings
from app.prompts.matcher import MATCHER_PROMPT
from app.schemas.verdict import MatchResult

logger = logging.getLogger(__name__)

# Errors worth retrying on another model: API errors (rate limit, model not found,
# server error), connection problems, and output that doesn't match the schema.

FALLBACK_ERRORS = (groq.APIStatusError, groq.APIConnectionError, OutputParserException)


def build_chain(model: str):
    if not settings.groq_api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set in the root .env file. "
            "Please set GROQ_API_KEY in your environment variables."
        )
    llm = ChatGroq(
        model=model,
        api_key=settings.groq_api_key,
        temperature=0,
    )
    return MATCHER_PROMPT | llm.with_structured_output(MatchResult)


def analyze(cv_text: str, job_text: str) -> MatchResult:
    inputs = {"cv": cv_text, "job": job_text}
    primary = settings.groq_model
    fallback = settings.groq_fallback_model

    try:
        return build_chain(primary).invoke(inputs)
    except FALLBACK_ERRORS as exc:
        if not fallback or fallback == primary:
            raise logger.warning(
                "Model %s failed (%s). Trying fallback %s.",
                primary,
                exc,
                fallback,
            ) from exc
        return build_chain(fallback).invoke(inputs)
