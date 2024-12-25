from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String, index=True)
    status = Column(String, default="New")
    call_frequency_days = Column(Integer, default=7)
    last_call_date = Column(DateTime, nullable=True)
    contacts = relationship("Contact", back_populates="lead")
    interactions = relationship("Interaction", back_populates="lead")

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    phone = Column(String)
    email = Column(String)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    lead = relationship("Lead", back_populates="contacts")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    interaction_type = Column(String)  # e.g. "call", "order"
    details = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    lead = relationship("Lead", back_populates="interactions")
