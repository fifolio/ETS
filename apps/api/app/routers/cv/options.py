from app.schemas.error_response import ErrorResponse

CV_ROUTER_OPTIONS = {
    "prefix": "/cv",
    "tags": ["cv"],
    "responses": {
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        403: {"model": ErrorResponse, "description": "The user's email isn't verified yet."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
}
