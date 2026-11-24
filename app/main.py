from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.config import settings
from app.infraestructure.email.service import EmailService
from app.infraestructure.files.service import S3Service


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.email_service = EmailService(settings.RESEND_API_KEY, settings.APP_NAME)
    app.state.s3_service = S3Service(
        settings.S3_ENDPOINT,
        settings.S3_ACCESS_KEY_ID,
        settings.S3_ACCESS_KEY_SECRET,
        settings.S3_PROJECT_REGION,
    )
    yield
    app.state.s3_service.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG,
)


app.include_router(api_router, prefix=settings.PEFIX)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
