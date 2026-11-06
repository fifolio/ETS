from fastapi.testclient import TestClient

from app.main import app
from app.schemas.public_testimonial import PublicTestimonial

client = TestClient(app)

SAMPLE = PublicTestimonial(
    id="row-1",
    quote="Saved me hours.",
    display_name="Jane D.",
    role="Nurse",
    hours_saved=1.7,
    scans=18,
)


def test_testimonials_are_public(monkeypatch):
    monkeypatch.setattr(
        "app.routers.testimonials.list_approved_testimonials", lambda limit: [SAMPLE]
    )

    response = client.get("/testimonials")

    assert response.status_code == 200
    assert response.json()[0]["quote"] == "Saved me hours."


def test_the_response_can_be_cached(monkeypatch):
    monkeypatch.setattr("app.routers.testimonials.list_approved_testimonials", lambda limit: [])

    assert "max-age" in client.get("/testimonials").headers["cache-control"]


def test_only_public_fields_are_exposed(monkeypatch):
    monkeypatch.setattr(
        "app.routers.testimonials.list_approved_testimonials", lambda limit: [SAMPLE]
    )

    keys = set(client.get("/testimonials").json()[0])

    assert keys == {"id", "quote", "display_name", "role", "hours_saved", "scans"}


def test_the_limit_is_validated():
    assert client.get("/testimonials?limit=500").status_code == 422
