class CVValidationError(Exception):
    """Raised when an uploaded CV can't be accepted. Carries one message per problem."""

    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = problems
