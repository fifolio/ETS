"""Static metadata shown in the auto-generated API docs (/docs and /redoc)."""

APP_TITLE = "ETS API"
APP_VERSION = "0.1.0"  # keep in sync with pyproject.toml
APP_SUMMARY = "AI-powered job post vs CV matching."

APP_DESCRIPTION = """
**ETS (Employment Targeting System)** helps job seekers decide fast whether a job post is worth
their time.

Send a job post and a candidate's CV, and the API returns a **smash or pass** verdict with a match
score, matching and missing skills, and red flags such as unrealistic requirements
(for example, "20 years of experience in AI").

## How it works
1. The candidate signs up and uploads a CV on the ETS web app.
2. The browser extension sends the job post text to this API.
3. An LLM compares the job with the CV and returns a structured verdict.

## Project status
Early development (alpha). Endpoints and response formats may change between versions.

## Links
- [Source code](https://github.com/fifolio/ETS)
- [Report an issue](https://github.com/fifolio/ETS/issues)

Open source under the MIT license.
"""

CONTACT = {
    "name": "Firas Dabbabi",
    "url": "https://www.linkedin.com/in/fifolio",
}

LICENSE_INFO = {
    "name": "MIT",
    "identifier": "MIT",
    "url": "https://github.com/fifolio/ETS/blob/main/LICENSE",
}

SERVERS = [
    {"url": "http://127.0.0.1:8000", "description": "Local development"},
    # Add the production URL here after deployment
]

TAGS_METADATA = [
    {
        "name": "health",
        "description": "Service status checks, used by hosting platforms and monitoring.",
    },
    # later add: {"name": "analyze", "description": "Job post vs CV matching."}
]