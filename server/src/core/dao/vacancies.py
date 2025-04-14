import sqlalchemy as alch

from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.vacancies.models import Vacancy
from src.companies.models import Company
from src.negotiations.models import Negotiation

async def fetch_vacancies_cards(
        session: AsyncSession,
        user_id: int = None,
        start: int = None,
        end: int = None
) -> Sequence:
    query = (
        alch.select(
            Vacancy.id,
            Vacancy.position,
            Vacancy.salary,
            Vacancy.company_id,
            Vacancy.author_id,
            Company.name.label("company_name"),
            Negotiation.id.label("negotiation_id"),
            Negotiation.status.label("negotiation_status")
        )
        .join(Company, Vacancy.company_id == Company.id)
        .join(
            Negotiation,
            alch.and_(
                Negotiation.vacancy_id == Vacancy.id,
                Negotiation.applicant_id == user_id
            ),
            isouter=True
        )
        .order_by(Vacancy.timestamp.desc())
        .slice(start, end)
    )
    
    result = await session.execute(query)
    return result.mappings().all()

async def count_vacancies(session: AsyncSession) -> int:
    query = (
        alch.select(func.count())
        .select_from(Vacancy)
    )
    
    result = await session.execute(query)
    return result.scalar()
