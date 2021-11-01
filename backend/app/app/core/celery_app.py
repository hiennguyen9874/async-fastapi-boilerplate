import os
from celery import Celery

from app.core.settings import settings


celery_app = Celery(
    "worker",
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
)
