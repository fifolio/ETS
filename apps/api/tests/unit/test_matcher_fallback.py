import groq
import httpx
import pytest
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import RunnableLambda

import app.chains.analyze as analyze_module
import app.chains.build_chain as build_chain_module
from app.chains.analyze import analyze
from app.core.config import settings
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict

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
        monkeypatch.setattr(analyze_module, "build_chain", lambda model: chains[model])
        monkeypatch.setattr(settings, "groq_model", "primary-model")
        monkeypatch.setattr(settings, "groq_fallback_model", "fallback-model")

    return _setup


def test_uses_primary_when_it_works(setup):
    primary = FakeChain(result=PRIMARY_RESULT)
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert analyze("cv", "job") == PRIMARY_RESULT
    assert fallback.calls == 0


def test_falls_back_on_rate_limit(setup):
    primary = FakeChain(error=rate_limit_error())
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert analyze("cv", "job") == FALLBACK_RESULT
    assert fallback.calls == 1


def test_falls_back_on_bad_model_output(setup):
    primary = FakeChain(error=OutputParserException("bad output"))
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(primary, fallback)

    assert analyze("cv", "job") == FALLBACK_RESULT


def test_raises_when_both_models_fail(setup):
    setup(FakeChain(error=rate_limit_error()), FakeChain(error=rate_limit_error()))

    with pytest.raises(groq.RateLimitError):
        analyze("cv", "job")


def test_does_not_fall_back_on_unrelated_errors(setup):
    fallback = FakeChain(result=FALLBACK_RESULT)
    setup(FakeChain(error=ValueError("a bug in our code")), fallback)

    with pytest.raises(ValueError):
        analyze("cv", "job")
    assert fallback.calls == 0


def test_build_chain_uses_the_requested_model(monkeypatch):
    captured = {}

    class FakeGroq:
        def __init__(self, model, **kwargs):
            captured["model"] = model

        def with_structured_output(self, schema):
            return RunnableLambda(lambda x: x)

    monkeypatch.setattr(build_chain_module, "ChatGroq", FakeGroq)
    monkeypatch.setattr(settings, "groq_api_key", "test-key")

    build_chain_module.build_chain("some-model")
    assert captured["model"] == "some-model"
