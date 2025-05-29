from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, JSON, DateTime, func
from enum import Enum as PyEnum
from app.core.database import Base

class OrgType(str, PyEnum):
    corporation     = "corporation"        # Frontend: "Corporation"
    small_business  = "small-business"     # Frontend: "Small Business"
    ngo             = "ngo"                # Frontend: "NGO/Non-Profit"
    government      = "government"         # Frontend: "Government Agency"
    investor        = "investor"           # Frontend: "Investor/Financial Institution"
    other           = "other"              

class PrimaryInterest(str, PyEnum):
    nature_based        = "nature-based"        # Frontend: 🌿 Nature-Based Solutions
    community_projects  = "community-projects"  # Frontend: 🏡 Community-Centric Projects
    renewable_energy    = "renewable-energy"    # Frontend: ⚡ Renewable Energy & IREC
    carbon_management   = "carbon-management"   # Frontend: 📊 Carbon Credit Management
    consultation        = "consultation"        # Frontend: 💬 General Consultation

class ContactInquiry(Base):
    __tablename__ = "contact_inquiries"

    id                  = Column(Integer, primary_key=True, index=True)
    full_name           = Column(String(120), nullable=False)
    email               = Column(String(255), nullable=False, index=True)
    company             = Column(String(255))
    phone               = Column(String(32))
    organization_type   = Column(Enum(OrgType), nullable=True)
    primary_interest    = Column(Enum(PrimaryInterest), nullable=True)
    subject             = Column(String(200), nullable=False)
    message             = Column(Text, nullable=False)
    areas_of_interest   = Column(JSON, nullable=True)    # list[str]
    communications_optin= Column(Boolean, default=False)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
