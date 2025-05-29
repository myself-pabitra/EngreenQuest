from sqlalchemy.orm import Session
from app.models.contact import ContactInquiry
from app.schemas.contact import ContactCreate

def create_contact(db: Session, req: ContactCreate) -> ContactInquiry:
    db_obj = ContactInquiry(
        full_name=req.full_name,
        email=req.email,
        company=req.company,
        phone=req.phone,
        organization_type=req.organization_type,
        primary_interest=req.primary_interest,
        subject=req.subject,
        message=req.message,
        areas_of_interest=req.areas_of_interest,
        communications_optin=req.communications_optin,
    )
    db.add(db_obj)
    return db_obj
