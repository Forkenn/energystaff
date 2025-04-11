from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_401, openapi_400
from src.core.dao.users import edit_user
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.users.schemas import SUserReadFull, SUserEdit

router = APIRouter(prefix='/users', tags=['Users'])

current_user = RoleManager(SystemRole.ACTIVE)

@router.get('/me', responses={**openapi_401})
async def get_current_user(
        user: User = Depends(current_user)
) -> SUserReadFull:
    return user

@router.post('/me', responses={**openapi_400})
async def edit_current_user(
        data: SUserEdit,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> SUserReadFull:
    user = await edit_user(session, user, data.model_dump())
    return user
