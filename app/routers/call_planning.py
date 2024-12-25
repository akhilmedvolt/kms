from fastapi import APIRouter, Depends
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
