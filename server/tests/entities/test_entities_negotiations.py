import pytest
from src.users.models import User
from src.companies.models import Company
from src.vacancies.models import Vacancy
from src.negotiations.models import Negotiation

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

@pytest.mark.asyncio
async def test_negotiation_creation(db_session: AsyncSession):
    """Test Negotiation creation"""
    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    user1 = User(email="emp@example.com", name="Emp", surname="Test", hashed_password="pwd", is_employer=True)
    user2 = User(email="app@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    db_session.add_all([user1, user2])
    await db_session.commit()

    vacancy = Vacancy(position="Dev", specialization="Backend", salary=100000, description="Some", author_id=user1.id, company_id=company.id)
    db_session.add(vacancy)
    await db_session.commit()

    n1 = Negotiation(applicant_id=2, employer_id=1, vacancy_id=1, status="pending")
    db_session.add(n1)
    await db_session.commit()

    assert n1.id == 1


@pytest.mark.asyncio
async def test_negotiation_unique_constraint(db_session: AsyncSession):
    """Test Negotiation unique for one user"""
    company = Company(name="CompanyX", inn="987654321012")
    db_session.add(company)
    await db_session.commit()

    user1 = User(email="emp@example.com", name="Emp", surname="Test", hashed_password="pwd", is_employer=True)
    user2 = User(email="app@example.com", name="App", surname="Test", hashed_password="pwd", is_applicant=True)
    db_session.add_all([user1, user2])
    await db_session.commit()

    vacancy = Vacancy(position="Dev", specialization="Backend", salary=100000, description="Some", author_id=user1.id, company_id=company.id)
    db_session.add(vacancy)
    await db_session.commit()

    n1 = Negotiation(applicant_id=2, employer_id=1, vacancy_id=1, status="pending")
    db_session.add(n1)
    await db_session.commit()

    n2 = Negotiation(applicant_id=2, employer_id=1, vacancy_id=1, status="pending")
    db_session.add(n2)
    with pytest.raises(IntegrityError):
        await db_session.commit()
