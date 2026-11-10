from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.constants.job_url import DEFAULT_PORTS
from app.services.scans.is_tracking_param import is_tracking_param


def normalize_job_url(url: str) -> str:
    """A stable form of a job page URL, so the same page always gives the same text."""
    text = url.strip()
    parts = urlsplit(text)
    scheme = parts.scheme.lower()
    if scheme not in DEFAULT_PORTS or not parts.netloc:
        return text.lower()
    try:
        port = parts.port
    except ValueError:
        return text.lower()

    host = (parts.hostname or "").lower().removeprefix("www.")
    netloc = host if port in (None, DEFAULT_PORTS[scheme]) else f"{host}:{port}"
    path = parts.path.rstrip("/") or "/"
    query = sorted(
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not is_tracking_param(key)
    )
    return urlunsplit((scheme, netloc, path, urlencode(query), ""))
