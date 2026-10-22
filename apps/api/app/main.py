from fastapi import FastAPI

from app.core import metadata
from app.core.errors import register_exception_handlers
from app.routers import analyze, cv, health

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

register_exception_handlers(app)
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(cv.router)
app.include_router(analyze.router)
