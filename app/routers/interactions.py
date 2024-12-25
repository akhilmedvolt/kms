from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user
from typing import List

router = APIRouter(prefix="/interactions", tags=["Interactions"])

# routers/interactions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user
from datetime import datetime

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

    # Create the interaction
    interaction = models.Interaction(**interaction_in.dict(), lead_id=lead.id)
    db.add(interaction)

    # If it's a CALL, update the lead's last_call_date
    if interaction.type == "CALL":
        # Option A: set last_call_date to the interaction_date
        lead.last_call_date = interaction.interaction_date
        # Option B: always use datetime.utcnow(), if you prefer
        # lead.last_call_date = datetime.utcnow()

    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/{lead_id}", response_model=List[schemas.InteractionResponse])
def list_interactions_for_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    interactions = db.query(models.Interaction).filter_by(lead_id=lead.id).all()
    return interactions
