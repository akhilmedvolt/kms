from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/call-planning", tags=["Call Planning"])

@router.get("/today", response_model=List[schemas.LeadResponse])
def leads_to_call_today(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Return the leads that require a call today.
    A lead requires a call if:
    - last_call_date is None (never called before), or
    - last_call_date + call_frequency_days <= today
    """
    today = datetime.utcnow()
    leads = db.query(models.Lead).all()

    leads_needing_calls = []
    for lead in leads:
        if not lead.last_call_date:
            leads_needing_calls.append(lead)
        else:
            next_call_due = lead.last_call_date + timedelta(
                days=lead.call_frequency_days
            )
            if next_call_due <= today:
                leads_needing_calls.append(lead)

    return leads_needing_calls

@router.get("/overdue", response_model=List[schemas.LeadResponse])
def overdue_calls(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Fetch leads with overdue calls.
    """
    today = datetime.utcnow()
    leads = db.query(models.Lead).filter(models.Lead.owner_id == current_user.id).all()

    overdue_leads = []
    for lead in leads:
        if lead.last_call_date:
            next_call_due = lead.last_call_date + timedelta(days=lead.call_frequency_days)
            if next_call_due < today:
                overdue_leads.append(lead)

    return overdue_leads

@router.put("/complete/{lead_id}", response_model=schemas.LeadResponse)
def mark_call_as_completed(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Update the last_call_date for a lead to mark a call as completed.
    """
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.owner_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.last_call_date = datetime.utcnow()
    db.commit()
    db.refresh(lead)
    return lead