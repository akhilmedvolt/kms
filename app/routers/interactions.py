from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user
from typing import List, Optional

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("/{lead_id}", response_model=schemas.InteractionResponse)
def add_interaction(
    lead_id: int,
    interaction_in: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):

    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    interaction_date = datetime.utcnow()
    interaction = models.Interaction(
        **interaction_in.dict(), lead_id=lead.id, interaction_date=interaction_date
    )
    db.add(interaction)

    if interaction.type == "CALL":
        lead.last_call_date = interaction_date

    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/{lead_id}", response_model=List[schemas.InteractionResponse])
def list_interactions_for_lead(
    lead_id: int,
    interaction_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    query = db.query(models.Interaction).filter_by(lead_id=lead.id)
    if interaction_type:
        query = query.filter(models.Interaction.type == interaction_type)

    return query.all()


@router.put("/{interaction_id}", response_model=schemas.InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction_in: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    interaction = (
        db.query(models.Interaction)
        .filter(models.Interaction.id == interaction_id)
        .first()
    )
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for attr, value in interaction_in.dict(exclude_unset=True).items():
        setattr(interaction, attr, value)

    db.commit()
    db.refresh(interaction)
    return interaction
