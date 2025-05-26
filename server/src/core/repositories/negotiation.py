import sqlalchemy as alch

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.common import CommonRepository
from src.users.models import User
from src.vacancies.models import Vacancy
from src.companies.models import Company
from src.negotiations.models import Negotiation, NegotiationStatus
from src.resume.models import Resume
from src.tools.models import Location


class NegotiationRepository(CommonRepository[Negotiation]):
    def __init__(self, session: AsyncSession):
        super().__init__(Negotiation, session)

    async def get_negotiations_applicant(
            self,
            applicant_id: int,
            start: int = None,
            end: int = None,
            status: NegotiationStatus = None
    ) -> Sequence[dict]:
        query = (
            alch.select(
                Negotiation.id,
                Negotiation.timestamp,
                Negotiation.status,
                Negotiation.vacancy_id,
                Negotiation.applicant_id,
                Negotiation.employer_description,
                Vacancy.position.label("vacancy_position"),
                Vacancy.salary.label("vacancy_salary"),
                Company.name.label("company_name")
            )
            .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
            .join(Company, Vacancy.company_id == Company.id)
            .where(Negotiation.applicant_id == applicant_id)
        )

        if status:
            query = query.where(Negotiation.status == status.value)

        if start and end:
            query = query.slice(start, end)

        result = await self.session.execute(
            query.order_by(Negotiation.timestamp.desc())
        )
        return result.mappings().all()
    
    async def count_negotiations_applicant(
            self, applicant_id: int, status: NegotiationStatus = None
    ) -> int:
        query = (
            alch.select(alch.func.count())
            .select_from(Negotiation)
            .where(Negotiation.applicant_id == applicant_id)
        )

        if status:
            query = query.where(Negotiation.status == status.value)

        result = await self.session.execute(query)
        return result.scalar()
    
    async def get_negotiations_employer(
            self,
            employer_id: int,
            start: int = None,
            end: int = None,
            status: NegotiationStatus = None
    ):
        query = (
            alch.select(
                Negotiation.id,
                Negotiation.timestamp,
                Negotiation.status,
                Negotiation.vacancy_id,
                Negotiation.applicant_id,
                Negotiation.employer_description,
                Vacancy.position.label("vacancy_position"),
                Vacancy.salary.label("vacancy_salary"),
                User.surname.label("user_surname"),
                User.last_name.label("user_last_name"),
                User.name.label("user_name"),
                Location.name.label("user_location")
            )
            .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
            .join(User, User.id == Negotiation.applicant_id)
            .join(Location, Location.id == User.location_id)
            .join(Resume, Resume.user_id == User.id)
            .where(Vacancy.author_id == employer_id)
        )

        if status:
            query = query.where(Negotiation.status == status.value)

        if start is not None and end is not None:
            query = query.slice(start, end)

        result = await self.session.execute(
            query.order_by(Negotiation.timestamp.desc())
        )
        return result.mappings().all()

    async def count_negotiations_employer(
            self, employer_id: int, status: NegotiationStatus = None
    ) -> int:
        query = (
            alch.select(alch.func.count())
            .select_from(Negotiation)
            .join(Vacancy, Negotiation.vacancy_id == Vacancy.id)
            .where(Vacancy.author_id == employer_id)
        )

        if status:
            query = query.where(Negotiation.status == status.value)

        result = await self.session.execute(query)
        return result.scalar()
    
    async def create(
            self, applicant_id: int, employer_id: int, vacancy_id: int
    ) -> Negotiation:
        negotiation = Negotiation(
            applicant_id=applicant_id,
            employer_id=employer_id,
            vacancy_id=vacancy_id
        )
        self.session.add(negotiation)
        await self.session.commit()
        return negotiation

    async def update(self,
            negotiation: Negotiation,
            status: NegotiationStatus,
            description: str = None
    ) -> None:
        negotiation.employer_description = description
        negotiation.status = status.value
        await self.session.commit()

    async def exists_by_vacancy_id(
            self,
            vacancy_id: int
    ) -> bool:
        query = alch.select(1).where(Negotiation.vacancy_id == vacancy_id)
        result = await self.session.scalar(query)
        return result is not None
