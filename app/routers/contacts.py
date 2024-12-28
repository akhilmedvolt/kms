from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/{lead_id}", response_model=schemas.ContactResponse)
def add_contact(
    lead_id: int,
    contact_in: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Ensure roles are unique for the lead
    existing_role = db.query(models.Contact).filter(
        models.Contact.lead_id == lead_id, models.Contact.role == contact_in.role
    ).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists for this lead")

    # Ensure email is valid (relies on Pydantic validation)
    contact = models.Contact(**contact_in.dict(), lead_id=lead_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.get("/{lead_id}", response_model=List[schemas.ContactResponse])
def list_contacts_for_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    contacts = db.query(models.Contact).filter(models.Contact.lead_id == lead_id).all()
    return contacts

@router.get("/search", response_model=List[schemas.ContactResponse])
def search_contacts(
    name: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    query = db.query(models.Contact).join(models.Lead).filter(models.Lead.owner_id == current_user.id)
    if name:
        query = query.filter(models.Contact.name.ilike(f"%{name}%"))
    if role:
        query = query.filter(models.Contact.role.ilike(f"%{role}%"))
    return query.all()
