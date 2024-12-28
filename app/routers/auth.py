# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import timedelta
from app.utils import get_password_hash, verify_password, create_access_token, create_email_verification_token, \
    verify_email_verification_token
from app.dependencies import get_current_active_user
from app.database import get_db
from app import models, schemas
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.email_utils import send_verification_email

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse)
async def register(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_create.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user_create.password)
    new_user = models.User(username=user_create.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate email verification token
    token = create_email_verification_token(data={"sub": new_user.username})

    # Send verification email
    await send_verification_email(email=new_user.username, username=new_user.username, token=token)

    return new_user


@router.post("/login", response_model=schemas.Token)
def login(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_create.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(user_create.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_active_user)):
    return current_user


@router.get("/verify-email", response_model=dict)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    token_data = verify_email_verification_token(token)
    if not token_data or not token_data.username:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if user.is_verified:
        return {"msg": "User already verified"}

    user.is_verified = True
    db.commit()
    return {"msg": "Email successfully verified"}
