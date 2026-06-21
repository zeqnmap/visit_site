from sqlalchemy.ext.asyncio import AsyncSession
from app.models.domain import ContactMessage
from app.schemas.contact import ContactCreate


class ContactService:
    @staticmethod
    async def create_message(db: AsyncSession, contact_data: ContactCreate):
        new_message = ContactMessage(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message
        )

        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)

        return new_message