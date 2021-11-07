import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import jwt

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.core.settings import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_TLS=settings.SMTP_TLS,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=settings.EMAIL_TEMPLATES_DIR,
)


async def send_email(
    email_to: str,
    subject: str = "",
    template_name: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=environment,
        subtype="html",
    )

    fm = FastMail(conf)

    await fm.send_message(message, template_name=template_name)

    logging.info(f"send email result")


async def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME

    subject = f"{project_name} - Test email"

    await send_email(
        email_to=email_to,
        subject=subject,
        template_name="test_email.html",
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    server_host = settings.SERVER_HOST

    link = f"{server_host}/reset-password?token={token}"

    await send_email(
        email_to=email_to,
        subject=subject,
        template_name="reset_password.html",
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


async def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"

    link = settings.SERVER_HOST

    await send_email(
        email_to=email_to,
        subject=subject,
        template_name="new_account.html",
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
