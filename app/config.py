# app/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load variables from .env

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "defaultsecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Email Configuration
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_TLS = os.getenv("MAIL_TLS", "true").lower() in ["true", "1", "yes"]
MAIL_SSL = os.getenv("MAIL_SSL", "false").lower() in ["true", "1", "yes"]
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "KAM Lead Management System")

# Email Templates Directory
EMAIL_TEMPLATES_DIR = Path(os.getenv("EMAIL_TEMPLATES_DIR", "templates/email"))
