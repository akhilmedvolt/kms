from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, nullable=False)
    status = Column(
        String, default="NEW"
    )  # Possible values: NEW, IN_PROGRESS, WON, LOST
    call_frequency_days = Column(Integer, default=7)  # how often KAM calls
    last_call_date = Column(DateTime)
    # Relationship
    contacts = relationship(
        "Contact", back_populates="lead", cascade="all, delete-orphan"
    )
    interactions = relationship(
        "Interaction", back_populates="lead", cascade="all, delete-orphan"
    )


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    lead = relationship("Lead", back_populates="contacts")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    interaction_date = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=False)
    type = Column(String, default="CALL")
    lead_id = Column(Integer, ForeignKey("leads.id"))
    lead = relationship("Lead", back_populates="interactions")
