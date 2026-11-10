import hashlib

from app.services.scans.normalize_job_url import normalize_job_url


def hash_job_url(url: str) -> str:
    """SHA-256 of the normalized URL: short, fixed length, and fine to index."""
    return hashlib.sha256(normalize_job_url(url).encode("utf-8")).hexdigest()
