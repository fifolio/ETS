import pytest

from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.schemas.job_board_suggestion_request import JobBoardSuggestionRequest
from app.services.suggestions.validate_suggestion import validate_suggestion


def make_request(**overrides):
    values = {"name": "Wellfound", "url": "https://wellfound.com/jobs/?ref=x"}
    return JobBoardSuggestionRequest(**{**values, **overrides})


def test_a_minimal_suggestion_is_cleaned():
    result = validate_suggestion(make_request(name="  Wellfound  "))

    assert (result.name, result.url) == ("Wellfound", "https://wellfound.com/jobs")
    assert result.example_url is None and result.country is None and result.notes is None


def test_an_example_link_on_the_same_site_is_kept_as_typed():
    example = "https://www.wellfound.com/jobs/1234-engineer?utm=a"

    result = validate_suggestion(
        make_request(example_url=f" {example} ", country=" Canada ", notes="Startups")
    )

    assert result.example_url == example
    assert (result.country, result.notes) == ("Canada", "Startups")


def test_a_name_that_is_too_short_is_refused():
    with pytest.raises(SuggestionRejectedError) as error:
        validate_suggestion(make_request(name=" x "))

    assert error.value.status_code == 422


def test_an_address_that_is_not_a_public_web_address_is_refused():
    with pytest.raises(SuggestionRejectedError) as error:
        validate_suggestion(make_request(url="http://localhost/jobs"))

    assert error.value.status_code == 422 and "web address" in error.value.message


def test_an_example_link_on_another_site_is_refused():
    with pytest.raises(SuggestionRejectedError) as error:
        validate_suggestion(make_request(example_url="https://other.com/jobs/1"))

    assert error.value.status_code == 422 and "same website" in error.value.message


def test_an_invalid_example_link_is_refused():
    with pytest.raises(SuggestionRejectedError) as error:
        validate_suggestion(make_request(example_url="not a link"))

    assert error.value.status_code == 422
