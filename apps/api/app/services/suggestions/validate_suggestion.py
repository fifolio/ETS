from app.constants.suggestions import MIN_NAME_LENGTH
from app.exceptions.suggestion_rejected_error import SuggestionRejectedError
from app.schemas.job_board_suggestion_request import JobBoardSuggestionRequest
from app.services.suggestions.get_site_host import get_site_host
from app.services.suggestions.normalize_board_url import normalize_board_url
from app.types.validated_suggestion import ValidatedSuggestion


def validate_suggestion(request: JobBoardSuggestionRequest) -> ValidatedSuggestion:
    """Check and clean a suggestion. Raises SuggestionRejectedError (422) for a bad one."""
    name = request.name.strip()
    if len(name) < MIN_NAME_LENGTH:
        raise SuggestionRejectedError("Enter the name of the job board.", 422)

    url = normalize_board_url(request.url)
    if url is None:
        raise SuggestionRejectedError(
            "Enter a valid web address that starts with http:// or https://.", 422
        )

    example = (request.example_url or "").strip() or None
    if example is not None:
        if normalize_board_url(example) is None:
            raise SuggestionRejectedError("The example job link isn't a valid web address.", 422)
        if get_site_host(example) != get_site_host(url):
            raise SuggestionRejectedError(
                "The example job link must be on the same website as the job board.", 422
            )

    return ValidatedSuggestion(
        name=name,
        url=url,
        example_url=example,
        country=(request.country or "").strip() or None,
        notes=(request.notes or "").strip() or None,
    )
