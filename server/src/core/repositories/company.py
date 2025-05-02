import sqlalchemy as alch

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
    
    async def get_companies_by_name(
            self, name: str, start: int, end: int
    ) -> Sequence[Company | None]:
        query = alch.select(Company)

        if name:
            query = query.where(Company.name.like(f"%{name}%"))

        query = query.order_by(Company.id.desc()).slice(start, end)

        return (await self.session.execute(query)).scalars().all()
    
    async def get_company_by_inn(self, inn: str) -> Company | None:
        query = alch.select(Company).where(Company.inn == inn)
        return (await self.session.execute(query)).scalar()
    
    async def delete_company(self, company: Company) -> None:
        await self.session.delete(company)
        await self.session.commit()

