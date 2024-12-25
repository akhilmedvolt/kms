from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app import schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=schemas.LeadResponse)
def create_lead(
    lead_in: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = models.Lead(**lead_in.dict())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/", response_model=List[schemas.LeadResponse])
def list_leads(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    leads = db.query(models.Lead).all()
    return leads


@router.get("/{lead_id}", response_model=schemas.LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    return lead


@router.put("/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(
    lead_id: int,
    lead_in: schemas.LeadUpdate,  # <-- now referencing LeadUpdate
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Only set fields that were provided in the PUT body
    for attr, value in lead_in.dict(exclude_unset=True).items():
        setattr(lead, attr, value)

    db.commit()
    db.refresh(lead)
    return lead


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
    return {"msg": "Lead deleted successfully"}
