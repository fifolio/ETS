from urllib.parse import urlsplit


def get_site_host(url: str) -> str:
    """The host of an address in lowercase without a leading www., or an empty text."""
    try:
        return (urlsplit(url.strip()).hostname or "").lower().removeprefix("www.")
    except ValueError:
        return ""
