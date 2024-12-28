# app/email_utils.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.config import (
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_TLS,
    MAIL_SSL,
    MAIL_FROM_NAME,
)
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_TLS=MAIL_TLS,
    MAIL_SSL=MAIL_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="templates/email",  # Optional: if using HTML templates
)


async def send_verification_email(email: EmailStr, username: str, token: str):
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"
    subject = "Verify Your Email"
    body = f"Hi {username},\n\nPlease verify your email by clicking on the following link:\n{verification_link}\n\nIf you did not sign up for this account, please ignore this email."

    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
