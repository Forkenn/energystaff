from fastapi import APIRouter, Depends

from src.deps import get_user_service
from src.responses import openapi_401, openapi_400, openapi_403, openapi_204, response_204
from src.core.schemas.common import SBaseQueryBody
from src.core.services.user import UserService
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
        user: User = Depends(current_user),
        user_service: UserService = Depends(get_user_service)
) -> SUserReadFull:
    await user_service.update_user(user, data)
    return user

@router.get('', responses={**openapi_400, **openapi_401, **openapi_403})
async def search_users(
        data: SBaseQueryBody = Depends(),
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
) -> SUsersPreview:
    users = await user_service.get_users_by_fullname(data)
    return {'count': len(users), 'items': users}

@router.delete('/{id}', responses={**openapi_204})
async def delete_user_by_id(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_by_id(int)
    return response_204

@router.get('/applicants', responses={**openapi_400, **openapi_401, **openapi_403})
async def get_applicants(
        data: SBaseQueryBody = Depends(),
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
) -> SApplicantsPreview:
    applicants = await user_service.get_applicants_by_fullname(user, data)
    return {'count': len(applicants), 'items': applicants}
