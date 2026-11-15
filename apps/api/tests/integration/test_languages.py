from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_the_languages_are_public_and_cached():
    response = client.get("/languages")

    assert response.status_code == 200
    assert "max-age=300" in response.headers["cache-control"]


def test_english_comes_first_and_is_translated():
    first = client.get("/languages").json()[0]

    assert first == {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "direction": "ltr",
        "translated": True,
    }


def test_right_to_left_languages_say_so():
    arabic = next(item for item in client.get("/languages").json() if item["code"] == "ar")

    assert arabic["direction"] == "rtl"
