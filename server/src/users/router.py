from fastapi import APIRouter, Depends

from src.deps import get_user_service
from src.responses import (
    openapi_401, openapi_400, openapi_403, openapi_204, response_204, openapi_404
)
from src.core.schemas.common import SBaseQueryCountResponse
from src.core.services.user import UserService
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.users.schemas import (
    SUserReadFull, SUserEdit, SUsersPreview, SApplicantsPreview,
    SApplicantsReadQuery, SApplicantsFilteredQuery, SApplicantPreview,
    SUsersFilteredQuery, SUsersReadQuery, SUserPreview
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
async def get_users(
        data: SUsersReadQuery = Depends(),
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
) -> SUsersPreview:
    users = await user_service.get_users_by_fullname(data)
    return {'count': len(users), 'items': users}

@router.get('/count', responses={**openapi_400, **openapi_401, **openapi_403})
async def get_users_count(
        data: SUsersFilteredQuery = Depends(),
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
) -> SBaseQueryCountResponse:
    count = await user_service.count_users_by_fullname(data)
    return {'count': count}

@router.delete('/{id}', responses={**openapi_204})
async def delete_user_by_id(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.delete_by_id(int)
    return response_204

@router.post('/{id}/deactivate', responses={**openapi_204})
async def deactivate_user_by_id(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.deactivate_user_by_id(id)
    return response_204

@router.post('/{id}/activate', responses={**openapi_204})
async def activate_user_by_id(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.activate_user_by_id(id)
    return response_204

@router.get('/applicants', responses={**openapi_400, **openapi_401, **openapi_403})
async def get_applicants(
        data: SApplicantsReadQuery = Depends(),
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
) -> SApplicantsPreview:
    applicants = await user_service.get_applicants_by_fullname(user, data)
    return {'count': len(applicants), 'items': applicants}

@router.get('/applicants/count', responses={**openapi_401, **openapi_403})
async def get_applicants_count(
        data: SApplicantsFilteredQuery = Depends(),
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
) -> SBaseQueryCountResponse:
    count = await user_service.count_applicants_by_fullname(user, data)
    return {'count': count}

@router.get('/applicants/{id}', responses={
    **openapi_401, **openapi_403, **openapi_404
})
async def get_applicant_by_id(
        id: int,
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
) -> SApplicantPreview:
    user = await user_service.get_applicant_by_id(user, id)
    return user

@router.get('/applicants/by-edu-id/{edu_num}', responses={
    **openapi_401, **openapi_403, **openapi_404
})
async def get_applicant_by_edu_number(
        edu_num: str,
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
) -> SApplicantPreview:
    user = await user_service.get_applicant_by_edu_num(user, edu_num)
    return user

@router.post('/applicants/{id}/verify', responses={**openapi_204})
async def verify_applicant(
        id: int,
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.verify_user_by_id(id)
    return response_204

@router.post('/applicants/{id}/unverify', responses={**openapi_204})
async def unverify_applicant(
        id: int,
        user: User = Depends(current_edu),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.unverify_user_by_id(id)
    return response_204

@router.post('/edu-workers/{id}/verify', responses={**openapi_204})
async def verify_edu(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.verify_user_by_id(id)
    return response_204

@router.post('/edu-workers/{id}/unverify', responses={**openapi_204})
async def unverify_edu(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.unverify_user_by_id(id)
    return response_204

@router.post('/employers/{id}/verify', responses={**openapi_204})
async def verify_employer(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.verify_user_by_id(id)
    return response_204

@router.post('/employers/{id}/unverify', responses={**openapi_204})
async def unverify_employer(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
):
    await user_service.unverify_user_by_id(id)
    return response_204

# This route position not wrong, it is a fix for the GET /users/applicants
@router.get('/{id}', responses={
    **openapi_400, **openapi_401, **openapi_403, **openapi_404
})
async def get_user_by_id(
        id: int,
        user: User = Depends(current_superuser),
        user_service: UserService = Depends(get_user_service)
) -> SUserPreview:
    data = await user_service.get_full_by_id(id)
    return data
