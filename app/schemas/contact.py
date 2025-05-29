from pydantic import BaseModel, EmailStr, Field, constr, validator
from typing import List, Optional
from enum import Enum
from app.models.contact import OrgType, PrimaryInterest



class ContactBase(BaseModel):
    full_name: str = Field(..., max_length=120)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = None
    organization_type: Optional[OrgType] = None
    primary_interest: Optional[PrimaryInterest] = None
    subject: str = Field(..., max_length=200)
    message: str = Field(..., min_length=30, max_length=10_000)
    areas_of_interest: Optional[List[str]] = Field(None, max_items=8)
    communications_optin: bool = False

    @validator("areas_of_interest", each_item=True)
    def aois_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Area of interest cannot be empty")
        return v.strip()

class ContactCreate(ContactBase):
    pass

class ContactInDB(ContactBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True

class ContactPublic(BaseModel):
    message: str
    id: int
