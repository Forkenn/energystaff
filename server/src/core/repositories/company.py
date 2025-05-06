import sqlalchemy as alch

from datetime import date
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.common import CommonRepository
from src.companies.models import Company


class CompanyRepository(CommonRepository[Company]):
    def __init__(self, session: AsyncSession):
        super().__init__(Company, session)

    async def update_company(self, company: Company, data: dict) -> Company:
        for field, value in data.items():
            setattr(company, field, value)

        await self.session.commit()
        return company
    
    async def _get_companies_by_name_query(
            self,
            query: alch.Select,
            registration_date: date  = None,
            only_verified: bool = False,
            q: str = None
    ) -> alch.Select:
        if registration_date:
            query = query.where(Company.registration_date == registration_date)

        if only_verified:
            query = query.where(Company.is_verified == True)

        if q:
            query = query.where(Company.name.like(f"%{q}%"))

        return query
    
    async def get_companies_by_name(
            self,
            registration_date: date  = None,
            only_verified: bool = False,
            q: str = None,
            start: int = None,
            end: int = None,
            desc: bool = True
    ) -> Sequence[Company | None]:
        query = alch.select(Company)
        query = await self._get_companies_by_name_query(
            query=query,
            registration_date=registration_date,
            only_verified=only_verified,
            q=q
        )

        if desc:
            query = query.order_by(Company.id.desc())
        else:
            query = query.order_by(Company.id.asc())

        query = query.slice(start, end)
        return (await self.session.execute(query)).scalars().all()
    
    async def count_companies_by_name(
            self,
            registration_date: date  = None,
            only_verified: bool = False,
            q: str = None
    ) -> int:
        query = alch.select(alch.func.count()).select_from(Company)
        query = await self._get_companies_by_name_query(
            query=query,
            registration_date=registration_date,
            only_verified=only_verified,
            q=q
        )

        result = await self.session.execute(query)
        return result.scalar()
    
    async def get_company_by_inn(self, inn: str) -> Company | None:
        query = alch.select(Company).where(Company.inn == inn)
        return (await self.session.execute(query)).scalar()
    
    async def delete_company(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()

