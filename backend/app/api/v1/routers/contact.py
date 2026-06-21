from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import ContactService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/", response_model=ContactResponse)
@limiter.limit("3/minute")
async def submit_contact_form(
        request: Request,
        contact: ContactCreate,
        db: AsyncSession = Depends(get_db)
):
    await ContactService.create_message(db, contact)

    return ContactResponse(
        status="success",
        message="Message received successfully. I will reach out soon!"
    )