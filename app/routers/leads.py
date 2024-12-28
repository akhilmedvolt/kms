from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user
import pytz
from datetime import datetime

router = APIRouter(prefix="/leads", tags=["Leads"])

def utc_to_local(utc_dt: datetime, timezone: str) -> datetime:
    """Convert UTC datetime to local timezone."""
    local_tz = pytz.timezone(timezone)
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)

@router.get("/", response_model=List[schemas.LeadResponse])
def list_leads(
    status: Optional[str] = None,
    kam_id: Optional[int] = None,
    timezone: Optional[str] = "UTC",  # New parameter for timezone
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    query = db.query(models.Lead).filter(models.Lead.owner_id == current_user.id)
    if status:
        query = query.filter(models.Lead.status == status)
    if kam_id:
        query = query.filter(models.Lead.kam_id == kam_id)

    leads = query.all()

    # Convert datetime fields to local timezone
    for lead in leads:
        if lead.last_call_date:
            lead.last_call_date = utc_to_local(lead.last_call_date, timezone)

    return leads

@router.post("/", response_model=schemas.LeadResponse)
def create_lead(
    lead: schemas.LeadCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)
):
    # Validate for duplicate entries
    existing_lead = db.query(models.Lead).filter(
        models.Lead.restaurant_name == lead.restaurant_name, models.Lead.owner_id == current_user.id
    ).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="A lead with this restaurant name already exists.")

    new_lead = models.Lead(owner_id=current_user.id, **lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@router.post("/assign-kam/{lead_id}", response_model=schemas.LeadResponse)
def assign_kam_to_lead(
    lead_id: int,
    kam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.owner_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    kam = db.query(models.KAM).filter(models.KAM.id == kam_id).first()
    if not kam:
        raise HTTPException(status_code=404, detail="KAM not found")

    lead.kam_id = kam_id
    db.commit()
    db.refresh(lead)
    return lead

@router.put("/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(
    lead_id: int,
    lead_in: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.owner_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Only update fields provided in the request
    for attr, value in lead_in.dict(exclude_unset=True).items():
        setattr(lead, attr, value)

    db.commit()
    db.refresh(lead)
    return lead