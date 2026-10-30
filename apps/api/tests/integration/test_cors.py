from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)

ALLOWED_ORIGIN = settings.cors_origins.split(",")[0].strip()


def test_preflight_from_an_allowed_origin_succeeds():
    response = client.options(
        "/analyze",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_preflight_from_an_unknown_origin_gets_no_permission():
    response = client.options(
        "/analyze",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert "access-control-allow-origin" not in response.headers
