from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI, echo=settings.DB_ECHO_LOG, future=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
