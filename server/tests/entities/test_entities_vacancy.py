import pytest
from src.users.models import User
from src.companies.models import Company
from src.vacancies.models import Vacancy, EmploymentFormat, EmploymentSchedule, EmploymentType
from src.tools.models import Location

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_vacancy_relationships(db_session: AsyncSession):
    """Test Vacancy all relationships"""
    user = User(email="vacancy@example.com", name="Vac", surname="Test", hashed_password="pwd", is_employer=True)
    db_session.add(user)
    await db_session.commit()

    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    location = Location(name="Talmberg")
    db_session.add(location)
    await db_session.commit()

    etype = EmploymentType(name="Full-time")
    eformat = EmploymentFormat(name="On-site")
    eschedule = EmploymentSchedule(name="Day shift")

    vacancy = Vacancy(
        position="QA",
        specialization="Manual testing",
        salary=75000,
        description="Check stuff",
        author_id=user.id,
        company_id=company.id,
        location_id=location.id,
        vacancy_types=[etype],
        vacancy_formats=[eformat],
        vacancy_schedules=[eschedule]
    )

    db_session.add(vacancy)
    await db_session.commit()
    await db_session.refresh(
        vacancy,
        attribute_names=(
            'vacancy_types',
            'vacancy_formats',
            'vacancy_schedules',
            'location',
            'company'
        )
    )

    assert vacancy.company.name == "CompanyX"
    assert vacancy.location.name == "Talmberg"
    assert vacancy.vacancy_types[0].name == "Full-time"
    assert vacancy.vacancy_formats[0].name == "On-site"
    assert vacancy.vacancy_schedules[0].name == "Day shift"


@pytest.mark.asyncio
async def test_vacancy_location_set_null(db_session: AsyncSession):
    """Test Vacancy set null on location delete"""
    user = User(email="vacancy@example.com", name="Vac", surname="Test", hashed_password="pwd", is_employer=True)
    db_session.add(user)
    await db_session.commit()

    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    location = Location(name="Talmberg")
    db_session.add(location)
    await db_session.commit()

    vacancy = Vacancy(
        position="QA",
        specialization="Manual testing",
        salary=75000,
        description="Check stuff",
        author_id=user.id,
        company_id=company.id,
        location_id=location.id,
    )

    db_session.add(vacancy)
    await db_session.commit()
    await db_session.refresh(vacancy, attribute_names=('location',))

    assert vacancy.company.name == "CompanyX"
    assert vacancy.location.name == "Talmberg"

    await db_session.delete(location)
    await db_session.commit()

    await db_session.refresh(vacancy, attribute_names=('location',))
    assert vacancy.location is None


@pytest.mark.asyncio
async def test_vacancy_type_delete(db_session: AsyncSession):
    """Test Vacancy delete EmploymentType"""
    user = User(email="vacancy@example.com", name="Vac", surname="Test", hashed_password="pwd", is_employer=True)
    db_session.add(user)
    await db_session.commit()

    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    etype = EmploymentType(name="Full-time")

    vacancy = Vacancy(
        position="QA",
        specialization="Manual testing",
        salary=75000,
        description="Check stuff",
        author_id=user.id,
        company_id=company.id,
        vacancy_types=[etype],
    )

    db_session.add(vacancy)
    await db_session.commit()
    await db_session.refresh(
        vacancy,
        attribute_names=(
            'vacancy_types',
        )
    )

    assert vacancy.vacancy_types[0].name == "Full-time"

    await db_session.delete(etype)
    await db_session.commit()

    await db_session.refresh(vacancy, attribute_names=('vacancy_types',))
    assert len(vacancy.vacancy_types) == 0


@pytest.mark.asyncio
async def test_vacancy_format_delete(db_session: AsyncSession):
    """Test Vacancy delete EmploymentFormat"""
    user = User(email="vacancy@example.com", name="Vac", surname="Test", hashed_password="pwd", is_employer=True)
    db_session.add(user)
    await db_session.commit()

    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    eformat = EmploymentFormat(name="On-site")
    eschedule = EmploymentSchedule(name="Day shift")

    vacancy = Vacancy(
        position="QA",
        specialization="Manual testing",
        salary=75000,
        description="Check stuff",
        author_id=user.id,
        company_id=company.id,
        vacancy_formats=[eformat],
    )

    db_session.add(vacancy)
    await db_session.commit()
    await db_session.refresh(
        vacancy,
        attribute_names=(
            'vacancy_formats',
        )
    )

    assert vacancy.vacancy_formats[0].name == "On-site"

    await db_session.delete(eformat)
    await db_session.commit()

    await db_session.refresh(vacancy, attribute_names=('vacancy_formats',))
    assert len(vacancy.vacancy_formats) == 0


@pytest.mark.asyncio
async def test_vacancy_schedule_delete(db_session: AsyncSession):
    """Test Vacancy delete EmploymentSchedule"""
    user = User(email="vacancy@example.com", name="Vac", surname="Test", hashed_password="pwd", is_employer=True)
    db_session.add(user)
    await db_session.commit()

    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    eschedule = EmploymentSchedule(name="Day shift")

    vacancy = Vacancy(
        position="QA",
        specialization="Manual testing",
        salary=75000,
        description="Check stuff",
        author_id=user.id,
        company_id=company.id,
        vacancy_schedules=[eschedule],
    )

    db_session.add(vacancy)
    await db_session.commit()
    await db_session.refresh(
        vacancy,
        attribute_names=(
            'vacancy_schedules',
        )
    )

    assert vacancy.vacancy_schedules[0].name == "Day shift"

    await db_session.delete(eschedule)
    await db_session.commit()

    await db_session.refresh(vacancy, attribute_names=('vacancy_schedules',))
    assert len(vacancy.vacancy_schedules) == 0
