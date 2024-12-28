from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class KAM(Base):
    __tablename__ = "kams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    leads = relationship("Lead", back_populates="kam")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Ensure this field exists
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Optional, for email verification

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    restaurant_name = Column(String, index=True)
    status = Column(String, default="NEW")
    call_frequency_days = Column(Integer, default=7)
    last_call_date = Column(DateTime, nullable=True)
    kam_id = Column(Integer, ForeignKey("kams.id"))  # Ensure this exists

    owner = relationship("User")
    kam = relationship("KAM", back_populates="leads")
    contacts = relationship("Contact", back_populates="lead", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="lead", cascade="all, delete-orphan")





class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"))  # Add this line
    lead = relationship("Lead", back_populates="contacts")  # Add this line

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    interaction_date = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=False)
    type = Column(String, default="CALL")
    outcome = Column(String, nullable=True)  # Optional Outcome Field
    lead_id = Column(Integer, ForeignKey("leads.id"))  # Add this line

    lead = relationship("Lead", back_populates="interactions")  # Add this line