from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
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
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    leads = db.query(models.Lead).filter(models.Lead.owner_id == current_user.id).all()
    good_leads = []
    for lead in leads:
        interactions_count = sum(
            1 for i in lead.interactions if i.interaction_date >= cutoff_date
        )
        if interactions_count > 5:
            good_leads.append(lead)
    return good_leads


@router.get("/under-performing", response_model=List[schemas.LeadResponse])
def under_performing_leads(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    leads = db.query(models.Lead).filter(models.Lead.owner_id == current_user.id).all()
    bad_leads = []
    for lead in leads:
        interactions_count = sum(
            1 for i in lead.interactions if i.interaction_date >= cutoff_date
        )
        if interactions_count < 3:
            bad_leads.append(lead)
    return bad_leads


@router.get("/visualizations/interaction-trends", response_model=Dict[str, int])
def interaction_trends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    interactions = (
        db.query(models.Interaction)
        .join(models.Lead)
        .filter(
            models.Lead.owner_id == current_user.id,
            models.Interaction.interaction_date >= cutoff_date,
        )
        .all()
    )

    trend_data = {}
    for interaction in interactions:
        date_key = interaction.interaction_date.strftime("%Y-%m-%d")
        if date_key not in trend_data:
            trend_data[date_key] = 0
        trend_data[date_key] += 1

    return trend_data


@router.get("/visualizations/order-patterns", response_model=Dict[str, int])
def order_patterns(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    interactions = (
        db.query(models.Interaction)
        .join(models.Lead)
        .filter(
            models.Lead.owner_id == current_user.id,
            models.Interaction.interaction_date >= cutoff_date,
        )
        .all()
    )

    pattern_data = {"CALL": 0, "ORDER": 0, "MEETING": 0}
    for interaction in interactions:
        if interaction.type in pattern_data:
            pattern_data[interaction.type] += 1

    return pattern_data
