import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "verysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kam_db.sqlite3")

# New configurations for email verification
EMAIL_VERIFICATION_SECRET_KEY = os.getenv(
    "EMAIL_VERIFICATION_SECRET_KEY", "anothersecretkey"
)
EMAIL_VERIFICATION_EXPIRE_HOURS = 24  # Token valid for 24 hours
# Email configurations
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = os.getenv("MAIL_TLS", "true").lower() in ["true", "1", "yes"]
MAIL_SSL = os.getenv("MAIL_SSL", "false").lower() in ["true", "1", "yes"]
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "KAM Lead Management System")
