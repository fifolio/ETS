from app.schemas.error_response import ErrorResponse

CV_ROUTER_OPTIONS = {
    "prefix": "/cv",
    "tags": ["cv"],
    "responses": {
        401: {"model": ErrorResponse, "description": "Missing or invalid token."},
        502: {"model": ErrorResponse, "description": "The storage service failed."},
        503: {"model": ErrorResponse, "description": "The service is not configured."},
    },
}
