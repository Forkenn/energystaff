import pytest
import pytest_asyncio

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NotFoundException
from src.users.models import User, Employer
from src.companies.schemas import SCompanyEdit
from src.companies.models import Company

from src.core.services.company import CompanyService


@pytest.mark.asyncio
async def test_get_or_create_company(company: Company, company_service: CompanyService):
    new_company = await company_service.get_company_or_create(company.name)
    assert new_company.id == company.id

    new_company = await company_service.get_company_or_create('CompanyX_1')
    assert new_company.id != company.id


@pytest.mark.asyncio
async def test_exists_company(company: Company, company_service: CompanyService):
    flag = await company_service.exists_company_by_name(company.name)
    assert flag == True

    flag = await company_service.exists_company_by_name('CompanyX_1')
    assert flag == False


@pytest.mark.asyncio
async def test_verify_company(db_session: AsyncSession, company: Company, company_service: CompanyService):
    await company_service.verify_company_by_id(company.id)
    await db_session.refresh(company)
    assert company.is_verified == True


@pytest.mark.asyncio
async def test_unverify_company(db_session: AsyncSession, company: Company, company_service: CompanyService):
    company.is_verified == True
    await db_session.commit()

    await company_service.unverify_company_by_id(company.id)
    await db_session.refresh(company)
    assert company.is_verified == False

@pytest.mark.asyncio
async def test_update_company(employer: User, company: Company, company_service: CompanyService):
    data = SCompanyEdit(
        name='CompanyX_test',
        registration_date=date(1994, 11, 3),
        inn='111111111111',
        address='Test Street, 62',
        description='Test_description_new'
    )

    new_company = await company_service.update_company(employer, company.id, data)

    assert new_company.name == 'CompanyX_test'
    assert new_company.registration_date == date(1994, 11, 3)
    assert new_company.inn == '111111111111'
    assert new_company.address == 'Test Street, 62'
    assert new_company.description == 'Test_description_new'


@pytest.mark.asyncio
async def test_update_company_not_found(employer: User, company: Company, company_service: CompanyService):
    data = SCompanyEdit(
        name='CompanyX_test',
        registration_date=date(1994, 11, 3),
        inn='111111111111',
        address='Test Street, 62',
        description='Test_description_new'
    )

    with pytest.raises(NotFoundException):
        await company_service.update_company(employer, 52, data)
