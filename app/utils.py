from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import os
from .schemas import TokenData

EMAIL_VERIFICATION_EXPIRE_HOURS = 24
EMAIL_VERIFICATION_SECRET_KEY = os.getenv("EMAIL_VERIFICATION_SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# New utility functions for email verification
def create_email_verification_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=EMAIL_VERIFICATION_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, EMAIL_VERIFICATION_SECRET_KEY, algorithm=ALGORITHM)


def verify_email_verification_token(token: str):
    try:
        payload = jwt.decode(
            token, EMAIL_VERIFICATION_SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username)
    except JWTError:
        return None
