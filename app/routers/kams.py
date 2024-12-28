from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/kams", tags=["KAM"])

@router.post("/", response_model=schemas.KAMResponse)
def create_kam(kam: schemas.KAMCreate, db: Session = Depends(get_db)):
    existing_kam = db.query(models.KAM).filter(models.KAM.email == kam.email).first()
    if existing_kam:
        raise HTTPException(status_code=400, detail="KAM with this email already exists")
    new_kam = models.KAM(**kam.dict())
    db.add(new_kam)
    db.commit()
    db.refresh(new_kam)
    return new_kam

@router.get("/", response_model=List[schemas.KAMResponse])
def get_kams(db: Session = Depends(get_db)):
    """
    Retrieve all KAMs.
    """
    return db.query(models.KAM).all()