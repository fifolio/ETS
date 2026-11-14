from urllib.parse import urlsplit

from app.services.suggestions.is_ip_host import is_ip_host

PRIVATE_SUFFIXES = (".local", ".localhost", ".internal", ".lan")


def normalize_board_url(url: str) -> str | None:
    """The cleaned main address (scheme, host, path), or None when it isn't a public web address."""
    try:
        parts = urlsplit(url.strip())
        host = (parts.hostname or "").lower()
        port = parts.port
    except ValueError:
        return None
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https") or not host:
        return None
    if parts.username or parts.password or port not in (None, 80, 443):
        return None
    if "." not in host or host == "localhost" or host.endswith(PRIVATE_SUFFIXES):
        return None
    if is_ip_host(host):
        return None
    return f"{scheme}://{host}{parts.path.rstrip('/')}"
