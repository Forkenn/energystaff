import sqlalchemy as alch

from typing import Sequence

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.vacancies.models import Vacancy
from src.companies.models import Company
from src.negotiations.models import Negotiation, NegotiationStatus

async def fetch_negotiations_applicant(
        session: AsyncSession,
        user_id: int,
        start: int = None,
        end: int = None,
        status: NegotiationStatus = None
) -> Sequence:
    query = (
        alch.select(
            Negotiation.id,
            Negotiation.timestamp,
            Negotiation.status,
            Negotiation.vacancy_id,
            Negotiation.applicant_id,
            Vacancy.position.label("vacancy_position"),
            Vacancy.salary.label("vacancy_salary"),
            Company.name.label("company_name")
        )
        .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
        .join(Company, Vacancy.company_id == Company.id)
        .where(Negotiation.applicant_id == user_id)
    )

    if status:
        query = query.where(Negotiation.status == status.value)

    if start and end:
        query = query.slice(start, end)

    result = await session.execute(query.order_by(Negotiation.timestamp.desc()))
    return result.mappings().all()

async def count_negotiations_applicant(
        session: AsyncSession,
        user_id: int,
        status: NegotiationStatus = None
) -> int:
    query = (
        alch.select(func.count())
        .select_from(Negotiation)
        .where(Negotiation.applicant_id == user_id)
    )

    if status:
        query = query.where(Negotiation.status == status.value)

    result = await session.execute(query)
    return result.scalar()

async def fetch_negotiations_employer(
        session: AsyncSession,
        user_id: int,
        start: int = None,
        end: int = None,
        status: NegotiationStatus = None
) -> Sequence:
    query = (
        alch.select(
            Negotiation.id,
            Negotiation.timestamp,
            Negotiation.status,
            Negotiation.vacancy_id,
            Negotiation.applicant_id,
            Vacancy.position.label("vacancy_position"),
            Vacancy.salary.label("vacancy_salary"),
            User.surname.label("user_surname"),
            User.last_name.label("user_last_name"),
            User.name.label("user_name")
        )
        .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
        .join(User, User.id == Negotiation.applicant_id)
        .where(Vacancy.author_id == user_id)
    )

    if status:
        query = query.where(Negotiation.status == status.value)

    if start and end:
        query = query.slice(start, end)

    result = await session.execute(query.order_by(Negotiation.timestamp.desc()))
    return result.mappings().all()

async def count_negotiations_employer(
        session: AsyncSession,
        user_id: int,
        status: NegotiationStatus = None
) -> int:
    query = (
        alch.select(func.count())
        .select_from(Negotiation)
        .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
        .where(Vacancy.author_id == user_id)
    )

    if status:
        query = query.where(Negotiation.status == status.value)

    result = await session.execute(query)
    return result.scalar()
