import sqlalchemy as alch

from typing import TypeVar, Type, Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.vacancies.models import Vacancy
from src.companies.models import Company

async def fetch_vacancies_cards(
        session: AsyncSession,
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
            Company.name.label("company_name")
        )
        .join(Company, Vacancy.company_id == Company.id)
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
