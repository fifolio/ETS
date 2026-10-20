from fastapi import FastAPI

from app.core import metadata
from app.routers import health

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

app.include_router(health.router)

