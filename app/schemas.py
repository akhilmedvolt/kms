from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# Auth Schemas
class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# Contact Schemas
class ContactBase(BaseModel):
    name: str
    role: str
    contact_info: str


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


# Interaction Schemas
class InteractionBase(BaseModel):
    details: str
    type: Optional[str] = "CALL"


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    id: int
    interaction_date: datetime

    class Config:
        orm_mode = True


# Lead Schemas
class LeadBase(BaseModel):
    restaurant_name: str
    status: Optional[str] = "NEW"
    call_frequency_days: Optional[int] = 7


class LeadCreate(LeadBase):
    pass


class LeadResponse(LeadBase):
    id: int
    last_call_date: Optional[datetime] = None
    contacts: List[ContactResponse] = []
    interactions: List[InteractionResponse] = []

    class Config:
        orm_mode = True


class LeadUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    status: Optional[str] = None
    call_frequency_days: Optional[int] = None
    last_call_date: Optional[datetime] = None
