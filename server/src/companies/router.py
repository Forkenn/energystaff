from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_404, openapi_403
from src.exceptions import NotFoundException, NotAllowedException
from src.core.dao.common import fetch_one
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.companies.models import Company
from src.companies.schemas import SCompanyEdit, SCompanyRead

router = APIRouter(prefix='/companies', tags=['Companies'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.EMPLOYER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/{id}', responses={**openapi_404, **openapi_403})
async def get_company_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> SCompanyRead:
    company: Company = await fetch_one(
        session,
        Company,
        where=(Company.id == id,)
    )

    if not company:
        raise NotFoundException()

    return company

@router.post('/{id}', responses={**openapi_404, **openapi_403})
async def edit_company_by_id(
    id: int,
    data: SCompanyEdit,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_employer)
) -> SCompanyRead:
    company: Company = await fetch_one(
        session,
        Company,
        where=(Company.id == id,)
    )

    if not company:
        raise NotFoundException()

    if company.id != user.employer.company_id:
        raise NotAllowedException()

    company.name = data.name
    company.address = data.address
    company.description = data.description
    company.inn = data.inn
    company.registration_date = data.registration_date

    await session.commit()
    return company
