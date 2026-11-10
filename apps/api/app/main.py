from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import metadata
from app.core.config import settings
from app.handlers.register_exception_handlers import register_exception_handlers
from app.routers import account, analyze, health, internal, onboarding, testimonials
from app.routers.catalog import industries, industry_jobs
from app.routers.cv import delete_cv, read_cv, upload_cv
from app.routers.feedback import eligibility, submit
from app.routers import stats

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
    allow_headers=["Authorization", "Content-Type"],
)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(upload_cv.router)
app.include_router(read_cv.router)
app.include_router(analyze.router)
app.include_router(delete_cv.router)
app.include_router(onboarding.router)
app.include_router(internal.router)
app.include_router(eligibility.router)
app.include_router(submit.router)
app.include_router(testimonials.router)
app.include_router(account.router)
app.include_router(industries.router)
app.include_router(industry_jobs.router)
app.include_router(stats.router)
