from fastapi import APIRouter, Depends

from src.deps import get_resume_service
from src.responses import openapi_404, openapi_204, openapi_400, response_204
from src.core.services.resume import ResumeService
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.resume.models import Resume
from src.resume.schemas import SResumeCreate, SResumeRead

router = APIRouter(prefix='/resume', tags=['Resume'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EMPLOYER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/me', responses={**openapi_404})
async def get_my_resume(
    user: User = Depends(current_user),
    resume_service: ResumeService = Depends(get_resume_service)
) -> SResumeRead:
    resume: Resume = await resume_service.get_full_resume_by_uid(user.id)

    return resume

@router.post('/me', responses={**openapi_400})
async def add_my_resume(
    data: SResumeCreate,
    user: User = Depends(current_user),
    resume_service: ResumeService = Depends(get_resume_service)
) -> SResumeRead:
    resume: Resume = await resume_service.create_resume(user.id, data)
    return resume

@router.patch('/me', responses={**openapi_404})
async def edit_my_resume(
        data: SResumeCreate,
        user: User = Depends(current_user),
        resume_service: ResumeService = Depends(get_resume_service)
) -> SResumeRead:
    resume: Resume = await resume_service.update_resume(user.id, data)
    return resume

@router.delete('/me', responses={**openapi_404, **openapi_204})
async def delete_my_resume(
        user: User = Depends(current_user),
        resume_service: ResumeService = Depends(get_resume_service)
):
    resume_service.delete_by_uid(user.id)
    return response_204

@router.get('')
async def get_resume_by_user_id(
        applicant_id: int,
        include_applicant: bool = False,
        user: User = Depends(current_employer),
        resume_service: ResumeService = Depends(get_resume_service)
) -> SResumeRead:
    resume: Resume = await resume_service.get_full_resume_by_uid_secured(
        user.id,
        applicant_id,
        include_applicant
    )

    return resume
