import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from app.core.settings import settings
from app.core.celery_app import celery_app

sentry_sdk.init(settings.SENTRY_DSN, integrations=[CeleryIntegration()])


@celery_app.task
def test_celery(word: str) -> str:
    return f"test task return {word}"
