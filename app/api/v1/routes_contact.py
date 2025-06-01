from fastapi import APIRouter, Depends, HTTPException, status,BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import contact as contact_schema
from app.crud import contact as crud_contact
import logging

from app.utility.email import send_admin_notification

router = APIRouter(prefix="/contact", tags=["Contact"])

log = logging.getLogger(__name__)


@router.post(
    "",
    response_model=contact_schema.ContactPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Inquiry saved successfully."},
        400: {"description": "Validation failed."},
        500: {"description": "Internal server error."},
    },
)
def submit_inquiry(
    payload: contact_schema.ContactCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    try:
        inquiry = crud_contact.create_contact(db, payload)
        db.flush()  # forces PK so we can return it
        # 👇 Send admin email in background
        background_tasks.add_task(send_admin_notification, payload.model_dump(mode="json"))

        log.info("New inquiry %s from %s", inquiry.id, inquiry.email)
        return {
            "message": "Thank you – our experts will get back to you shortly.",
            "id": inquiry.id,
        }
    except Exception as exc:
        import traceback

        traceback.print_exc()
        log.exception("Failed to create inquiry ")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred – please try again later.",
        ) from exc
