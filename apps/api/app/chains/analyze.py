import logging

from app.chains.build_chain import build_chain
from app.constants.matcher import FALLBACK_ERRORS
from app.core.config import settings
from app.schemas.match_result import MatchResult

logger = logging.getLogger(__name__)


def analyze(cv_text: str, job_text: str) -> MatchResult:
    inputs = {"cv": cv_text, "job": job_text}
    primary = settings.groq_model
    fallback = settings.groq_fallback_model

    try:
        return build_chain(primary).invoke(inputs)
    except FALLBACK_ERRORS as exc:
        if not fallback or fallback == primary:
            raise
        logger.warning("Model %s failed (%s). Trying fallback %s.", primary, exc, fallback)
        return build_chain(fallback).invoke(inputs)
