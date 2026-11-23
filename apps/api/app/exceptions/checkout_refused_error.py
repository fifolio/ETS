class CheckoutRefusedError(Exception):
    """The requested purchase isn't allowed. Carries a message for the user."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
