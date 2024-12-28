import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
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
    EMAIL_TEMPLATES_DIR
)
from pathlib import Path

# Initialize Jinja2 Environment (Optional: Only if using HTML templates)
env = Environment(
    loader=FileSystemLoader(searchpath=EMAIL_TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml'])
)

async def send_verification_email(email: EmailStr, username: str, token: str):
    verification_link = f"http://localhost:8000/auth/verify-email?token={token}"
    subject = "Verify Your Email"

    # Render HTML Template (Optional)
    # template = env.get_template('verification.html')
    # html_content = template.render(username=username, verification_link=verification_link)

    # Plain Text Email
    body = f"""Hi {username},

Please verify your email by clicking on the following link:
{verification_link}

If you did not sign up for this account, please ignore this email.
"""

    # Create EmailMessage
    message = EmailMessage()
    message["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM}>"
    message["To"] = email
    message["Subject"] = subject
    message.set_content(body)
    # If using HTML templates, uncomment the following line:
    # message.add_alternative(html_content, subtype='html')

    try:
        await aiosmtplib.send(
            message,
            hostname=MAIL_SERVER,
            port=MAIL_PORT,
            username=MAIL_USERNAME,
            password=MAIL_PASSWORD,
            start_tls=MAIL_TLS
        )
        print(f"Verification email sent to {email}")
    except aiosmtplib.SMTPException as e:
        print(f"Failed to send email to {email}: {e}")
