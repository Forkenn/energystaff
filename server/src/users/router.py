from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.manager import fastapi_users
from src.database import get_async_session

from src.users.models import User
from src.users.schemas import SUserReadFull

router = APIRouter(prefix='/users', tags=['Users'])

current_user = fastapi_users.current_user(active=True)

@router.get('/me')
async def get_current_user(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> SUserReadFull:
    await session.refresh(user, ('applicant', 'employer', 'edu_worker'))
    return user
