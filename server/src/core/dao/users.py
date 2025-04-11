from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User

async def edit_user(session: AsyncSession, user: User, data: dict) -> User:
    for field, value in data.items():
        setattr(user, field, value)

    await session.commit()
    return user
