from fastapi import APIRouter, Depends

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_404, openapi_403, openapi_204, openapi_400, response_204
from src.exceptions import NotFoundException, AlreadyExistException, NotAllowedException
from src.core.dao.common import fetch_all, fetch_one
from src.core.dao.resume import get_secure_resume
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.vacancies.models import EmploymentFormat, EmploymentType
from src.resume.models import Resume
from src.resume.schemas import SResumeCreate, SResumeRead

router = APIRouter(prefix='/resume', tags=['Resume'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EMPLOYER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/me', responses={**openapi_404})
async def get_my_resume(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SResumeRead:
    resume: Resume = await fetch_one(
        session,
        Resume,
        where=(Resume.user_id == user.id,),
        options=(
            joinedload(Resume.resume_formats),
            joinedload(Resume.resume_types)
        )
    )
    if not resume:
        raise NotFoundException()
    
    return resume

@router.post('/me', responses={**openapi_400})
async def add_my_resume(
    data: SResumeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SResumeRead:
    resume: Resume = await fetch_one(
        session,
        Resume,
        where=(Resume.user_id == user.id,),
        options=(
            joinedload(Resume.resume_formats),
            joinedload(Resume.resume_types)
        )
    )
    if resume:
        raise AlreadyExistException()

    formats = await fetch_all(
        session,
        EmploymentFormat,
        EmploymentFormat.id.in_(data.resume_formats_ids)
    )
    types = await fetch_all(
        session,
        EmploymentType,
        EmploymentType.id.in_(data.resume_types_ids)
    )

    new_resume = Resume(
        position=data.position,
        specialization=data.specialization,
        salary=data.salary,
        description=data.description,
        user_id=user.id
    )

    new_resume.resume_formats = formats
    new_resume.resume_types = types

    session.add(new_resume)
    await session.commit()
    return new_resume

@router.patch('/me', responses={**openapi_404})
async def edit_my_resume(
        data: SResumeCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> SResumeRead:
    resume: Resume = await fetch_one(
        session,
        Resume,
        where=(Resume.user_id == user.id,),
        options=(
            joinedload(Resume.resume_formats),
            joinedload(Resume.resume_types)
        )
    )
    if not resume:
        raise NotFoundException()

    formats = await fetch_all(
        session,
        EmploymentFormat,
        EmploymentFormat.id.in_(data.resume_formats_ids)
    )
    types = await fetch_all(
        session,
        EmploymentType,
        EmploymentType.id.in_(data.resume_types_ids)
    )

    resume.position = data.position
    resume.specialization = data.specialization
    resume.description = data.description
    resume.salary = data.salary
    resume.resume_formats = formats
    resume.resume_types = types
    await session.commit()
    
    return resume

@router.delete('/me', responses={**openapi_404, **openapi_204})
async def delete_my_resume(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    resume: Resume = await fetch_one(
        session,
        Resume,
        where=(Resume.user_id == user.id,)
    )
    if not resume:
        raise NotFoundException()
    
    await session.delete(resume)
    await session.commit()
    return response_204

@router.get('')
async def get_resume_by_user_id(
        applicant_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_employer)
) -> SResumeRead:
    resume: Resume = await get_secure_resume(
        session,
        user.id,
        applicant_id
    )

    if not resume:
        raise NotFoundException()

    return resume
