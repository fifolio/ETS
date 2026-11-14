class SuggestionRejectedError(Exception):
    """A suggestion can't be accepted. Carries a message for the user and an HTTP status."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
