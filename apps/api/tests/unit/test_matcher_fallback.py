import groq
import httpx
import pytest
from langchain_core.exceptions import OutputParserException

from app.chains import matcher
from app.schemas.verdict import MatchResult, Verdict

PRIMARY_RESULT = MatchResult(
    verdict=Verdict.SMASH,
    score=90,
    summary="Primary says smash.",
    matching_skills=[],
    missing_skills=[],
    red_flags=[],
)
FALLBACK_RESULT = PRIMARY_RESULT.model_copy(update={"score": 70, "summary": "Fallback says smash."})


class FakeChain:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = 0

    def invoke(self, inputs):
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


def rate_limit_error():
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    response = httpx.Response(429, request=request)
    return groq.RateLimitError("rate limited", response=response, body=None)


@pytest.fixture
def setup(monkeypatch):
    def _setup(primary: FakeChain, fallback: FakeChain):
        chains = {"primary-model": primary, "fallback-model": fallback}
        monkeypatch.setattr(matcher, "build_chain", lambda model: chains[model])
        monkeypatch.setattr(matcher.settings, "groq_model", "primary-model")
        monkeypatch.setattr(matcher.settings, "groq_fallback_model", "fallback-model")

    return _setup


def test_uses_primary_when_it_works(setup):
    primary = FakeChain(result=PRIMARY_RESULT)
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert matcher.analyze("cv", "job") == PRIMARY_RESULT
    assert fallback.calls == 0


def test_falls_back_on_rate_limit(setup):
    primary = FakeChain(error=rate_limit_error())
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert matcher.analyze("cv", "job") == FALLBACK_RESULT
    assert fallback.calls == 1


def test_falls_back_on_bad_model_output(setup):
    primary = FakeChain(error=OutputParserException("bad output"))
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert matcher.analyze("cv", "job") == FALLBACK_RESULT


def test_raises_when_both_models_fail(setup):
    setup(FakeChain(error=rate_limit_error()), FakeChain(error=rate_limit_error()))

    with pytest.raises(groq.RateLimitError):
        matcher.analyze("cv", "job")


def test_does_not_fall_back_on_unrelated_errors(setup):
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(FakeChain(error=ValueError("a bug in our code")), fallback)

    with pytest.raises(ValueError):
        matcher.analyze("cv", "job")
    assert fallback.calls == 0
