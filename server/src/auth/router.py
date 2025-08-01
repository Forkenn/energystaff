from fastapi import APIRouter, Request, Depends
from fastapi_users.exceptions import UserAlreadyExists

from src.deps import get_user_service, get_institutions_service
from src.exceptions import AlreadyExistException
from src.responses import openapi_400, openapi_404, openapi_204, response_204
from src.core.services.user import UserService
from src.core.services.company import CompanyService
from src.core.repositories.company import CompanyRepository
from src.core.services.catalog import CatalogService
from src.auth.roles import SystemRole, RoleManager
from src.auth.manager import fastapi_users, UserManager
from src.auth.schemas import (
    SUserRead, SUserCreateBase, SUserCreate, SEmployerCreate, SEduCreate,
    SUserPasswordChange, SUserEmailChange
)
from src.auth.tools import create_user_role
from src.users.models import User

router = APIRouter(prefix='/auth', tags=['Auth'])

current_user = RoleManager(SystemRole.ACTIVE)

@router.post('/change-password', responses={**openapi_400, **openapi_204})
async def change_password(
    data: SUserPasswordChange,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(fastapi_users.get_user_manager)
):
    await user_manager.update_password(user, data.old_password, data.new_password)
    return response_204

@router.post('/change-email', responses={**openapi_400, **openapi_204})
async def change_email(
    data: SUserEmailChange,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(fastapi_users.get_user_manager)
):
    try:
        await user_manager.update_email(user, data.new_email, data.password)
    except UserAlreadyExists:
        raise AlreadyExistException()

    return response_204

@router.post('/applicant/register', responses={**openapi_400})
async def register_applicant(
    request: Request,
    user_data: SUserCreateBase,
    user_manager: UserManager = Depends(fastapi_users.get_user_manager),
    user_service: UserService = Depends(get_user_service)
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

    await user_service.create_applicant(new_user)
    return new_user

@router.post('/employer/register', responses={**openapi_400, **openapi_404})
async def register_employer(
    request: Request,
    user_data: SEmployerCreate,
    user_manager: UserManager = Depends(fastapi_users.get_user_manager),
    user_service: UserService = Depends(get_user_service)
) -> SUserRead:
    company_repo = CompanyRepository(user_service.repository.session)
    company_service = CompanyService(company_repo)

    if user_data.company_id:
        company = await company_service.get_by_id(user_data.company_id)

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

    if user_data.company_name:
        company = await company_service.get_company_or_create(user_data.company_name)

    await user_service.create_employer(new_user, company.id)
    return new_user

@router.post('/edu/register', responses={**openapi_400, **openapi_404})
async def register_edu(
    request: Request,
    user_data: SEduCreate,
    user_manager: UserManager = Depends(fastapi_users.get_user_manager),
    user_service: UserService = Depends(get_user_service),
    inst_service: CatalogService = Depends(get_institutions_service)
) -> SUserRead:
    edu_institution = await inst_service.get_by_id(user_data.edu_institution_id)
    
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

    await user_service.create_edu_worker(new_user, edu_institution.id)
    return new_user
