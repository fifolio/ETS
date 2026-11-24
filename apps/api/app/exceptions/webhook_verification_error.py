class WebhookVerificationError(Exception):
    """The webhook isn't authentic, is too old, or can't be read."""
