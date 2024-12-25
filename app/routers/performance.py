from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/performance", tags=["Performance"])


@router.get("/well-performing", response_model=List[schemas.LeadResponse])
def well_performing_leads(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Dummy logic: well-performing leads have more than 2 calls or orders in the last 30 days.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    leads = db.query(models.Lead).all()
    good_leads = []
    for lead in leads:
        interactions_count = sum(
            1 for i in lead.interactions if i.interaction_date >= cutoff_date
        )
        if interactions_count > 2:
            good_leads.append(lead)
    return good_leads


@router.get("/under-performing", response_model=List[schemas.LeadResponse])
def under_performing_leads(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Dummy logic: under-performing leads have 1 or fewer interactions in the last 30 days.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    leads = db.query(models.Lead).all()
    bad_leads = []
    for lead in leads:
        interactions_count = sum(
            1 for i in lead.interactions if i.interaction_date >= cutoff_date
        )
        if interactions_count <= 1:
            bad_leads.append(lead)
    return bad_leads
