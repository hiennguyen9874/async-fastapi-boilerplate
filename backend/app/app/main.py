import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core.settings import settings
from app.api.api_v1.api import api_router

sentry_sdk.init(settings.SENTRY_DSN)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.add_middleware(SentryAsgiMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
