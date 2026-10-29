from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import metadata
from app.core.errors import register_exception_handlers
from app.routers import analyze, cv, health
from app.core.config import settings

app = FastAPI(
    title=metadata.APP_TITLE,
    summary=metadata.APP_SUMMARY,
    description=metadata.APP_DESCRIPTION,
    version=metadata.APP_VERSION,
    contact=metadata.CONTACT,
    license_info=metadata.LICENSE_INFO,
    servers=metadata.SERVERS,
    openapi_tags=metadata.TAGS_METADATA,
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)

register_exception_handlers(app)
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(cv.router)
app.include_router(analyze.router)
