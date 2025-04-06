from fastapi import APIRouter, HTTPException, status, Request, Depends

import sqlalchemy as alch
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.manager import fastapi_users, UserManager
from src.auth.schemas import (
    SUserRead, SUserCreateBase, SUserCreate, SEmployerCreate, SEduCreate
)
from src.auth.tools import create_user_role
from src.users.models import User, Applicant, Employer, EduWorker
from src.companies.models import Company
from src.tools.models import EduInstitution

router = APIRouter(prefix='/auth', tags=['Auth'])

responses ={
    404: {"description": "Item not found"},
    401: {"description": "Missing token or inactive/unverified user."},
    400: {"description": "Bad Request"},
    204: {"description": "Successful Response"},
    202: {"description": "Successful Response"}
}

@router.post('/applicant/register')
async def register_applicant(
    request: Request,
    user_data: SUserCreateBase,
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(fastapi_users.get_user_manager)
) -> SUserRead:
    user_create_schema = SUserCreate(
        surname=user_data.surname,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        is_applicant=True
    )
    new_user: User = await create_user_role(
        request, user_create_schema, user_manager
    )
    new_user.applicant = Applicant(user_id=new_user.id)
    await session.commit()

    return new_user

@router.post('/employer/register')
async def register_employer(
    request: Request,
    user_data: SEmployerCreate,
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(fastapi_users.get_user_manager)
) -> SUserRead:
    
    if user_data.company_id:
        company = await session.get(Company, user_data.company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Company does not exist'
            )

    if user_data.company_name:
        query = alch.select(Company).where(Company.name == user_data.company_name)
        company = (await session.execute(query)).scalar()

    user_create_schema = SUserCreate(
        surname=user_data.surname,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        is_employer=True
    )
    new_user: User = await create_user_role(
        request, user_create_schema, user_manager
    )
    if not company:
        company = Company(name=user_data.company_name)
        session.add(company)
        await session.commit()

    new_user.employer = Employer(company_id=company.id)
    await session.commit()

    return new_user

@router.post('/edu/register')
async def register_edu(
    request: Request,
    user_data: SEduCreate,
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(fastapi_users.get_user_manager)
) -> SUserRead:
    edu_institution = await session.get(EduInstitution, user_data.edu_institution_id)
    if not edu_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Edu Institution does not exist'
        )
    
    user_create_schema = SUserCreate(
        surname=user_data.surname,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        is_edu=True
    )
    new_user: User = await create_user_role(
        request, user_create_schema, user_manager
    )

    new_user.edu_worker = EduWorker(edu_institution_id=user_data.edu_institution_id)
    await session.commit()

    return new_user
