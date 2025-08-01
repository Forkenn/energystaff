from fastapi import APIRouter, Depends

from src.responses import openapi_404, openapi_403, openapi_204, response_204
from src.deps import get_company_service
from src.core.services.company import CompanyService
from src.core.schemas.common import SBaseQueryCountResponse
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.companies.models import Company
from src.companies.schemas import (
    SCompanyEdit, SCompanyRead, SCompaniesRead, SComaniesReadQuery,
    SComaniesFilteredQuery
)

router = APIRouter(prefix='/companies', tags=['Companies'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.EMPLOYER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('')
async def get_companies(
    data: SComaniesReadQuery = Depends(),
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
) -> SCompaniesRead:
    companies = await company_service.get_companies_by_name(data)
    return {'count': len(companies), 'items': companies}

@router.get('/count')
async def get_companies_count(
    data: SComaniesFilteredQuery = Depends(),
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
) -> SBaseQueryCountResponse:
    count = await company_service.count_companies_by_name(data)
    return {'count': count}

@router.get('/{id}', responses={**openapi_404, **openapi_403})
async def get_company_by_id(
    id: int,
    user: User = Depends(current_user),
    company_service: CompanyService = Depends(get_company_service)
) -> SCompanyRead:
    company = await company_service.get_by_id(id)
    return company

@router.get('/by-inn/{inn}', responses={**openapi_404})
async def get_company_by_inn(
    inn: str,
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
) -> SCompanyRead:
    company = await company_service.get_company_by_inn(inn)
    return company

@router.post('/{id}', responses={**openapi_404, **openapi_403})
async def edit_company_by_id(
    id: int,
    data: SCompanyEdit,
    user: User = Depends(current_employer),
    company_service: CompanyService = Depends(get_company_service)
) -> SCompanyRead:
    company: Company = await company_service.update_company(user, id, data)
    return company

@router.post('/{id}/verify', responses={**openapi_204, **openapi_403})
async def verify_company_by_id(
    id: int,
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
):
    await company_service.verify_company_by_id(id)
    return response_204

@router.post('/{id}/unverify', responses={**openapi_204, **openapi_403})
async def unverify_company_by_id(
    id: int,
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
):
    await company_service.unverify_company_by_id(id)
    return response_204

@router.delete('/{id}', responses={**openapi_204})
async def delete_company_by_id(
    id: int,
    user: User = Depends(current_superuser),
    company_service: CompanyService = Depends(get_company_service)
):
    await company_service.delete_by_id(id)
    return response_204
