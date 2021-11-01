from typing import Optional, Dict, Any
from pydantic import (
    BaseSettings,
    AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    validator,
    HttpUrl,
)


class Settings(BaseSettings):
    TIME_ZONE: str

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> Optional[str]:
        return (
            self.SQLALCHEMY_DATABASE_URI.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
            if self.SQLALCHEMY_DATABASE_URI
            else self.SQLALCHEMY_DATABASE_URI
        )

    DB_ECHO_LOG: bool = False

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),  # type: ignore
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    class Config:
        case_sensitive = True


settings = Settings()
