from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token, UserResponse
from app.utils import get_password_hash, verify_password, create_access_token
from app.dependencies import get_current_active_user
from app.database import get_db
from app import models
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app import models, schemas

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.username == user_create.username)
        .first()
    )
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user_create.password)
    new_user = models.User(username=user_create.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user_create: UserCreate, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.username == user_create.username)
        .first()
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(user_create.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def me(current_user: models.User = Depends(get_current_active_user)):
    return current_user
