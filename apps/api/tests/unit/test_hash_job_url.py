from app.services.scans.hash_job_url import hash_job_url


def test_the_same_page_gives_the_same_hash_however_it_was_reached():
    first = hash_job_url("https://example.com/jobs/123?utm_source=newsletter")
    second = hash_job_url("https://www.example.com/jobs/123/#apply")

    assert first == second


def test_different_jobs_give_different_hashes():
    assert hash_job_url("https://example.com/job?id=1") != hash_job_url(
        "https://example.com/job?id=2"
    )


def test_the_hash_is_64_hex_characters():
    value = hash_job_url("https://example.com/jobs/1")

    assert len(value) == 64
    assert int(value, 16) >= 0
