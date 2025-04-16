from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_401, openapi_400, openapi_403
from src.core.dao.users import edit_user, fetch_applicants, fetch_users
from src.core.dao.common import fetch_all
from src.core.schemas.common import SBaseQueryBody
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.users.schemas import (
    SUserReadFull, SUserEdit, SUsersPreview, SApplicantsPreview
)

router = APIRouter(prefix='/users', tags=['Users'])

current_user = RoleManager(SystemRole.ACTIVE)
current_edu = RoleManager(SystemRole.ACTIVE, SystemRole.VERIFIED, SystemRole.EDU_WORKER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/me', responses={**openapi_401})
async def get_current_user(
        user: User = Depends(current_user)
) -> SUserReadFull:
    return user

@router.post('/me', responses={**openapi_400, **openapi_401})
async def edit_current_user(
        data: SUserEdit,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> SUserReadFull:
    user = await edit_user(session, user, data.model_dump())
    return user

@router.get('', responses={**openapi_400, **openapi_401, **openapi_403})
async def get_users(
        data: SBaseQueryBody = Depends(),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_superuser)
) -> SUsersPreview:
    users = await fetch_users(session, data.q, data.start, data.end)
    return {'count': len(users), 'items': users}

@router.get('/applicants', responses={**openapi_400, **openapi_401, **openapi_403})
async def get_applicants(
        data: SBaseQueryBody = Depends(),
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_edu)
) -> SApplicantsPreview:
    applicants = await fetch_applicants(session, user, data.q, data.start, data.end)
    return {'count': len(applicants), 'items': applicants}
