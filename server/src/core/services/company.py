from typing import Sequence

from src.exceptions import NotFoundException, NotAllowedException
from src.core.services.common import CommonService
from src.core.repositories.company import CompanyRepository
from src.users.models import User
from src.companies.models import Company
from src.companies.schemas import SCompanyEdit, SComaniesReadQuery, SComaniesFilteredQuery


class CompanyService(CommonService[CompanyRepository]):
    def __init__(self, company_repo: CompanyRepository):
        super().__init__(company_repo)

    async def get_company_or_create(self, name: str) -> Company:
        company: Company = await self.repository.get_company_by_name(name)

        if not company:
            company = await self.repository.create_company(name)

        return company
    
    async def exists_company_by_name(self, name: str) -> bool:
        return await self.repository.exists_company_by_name(name)

    async def update_company(self, user: User, company_id: int, data: SCompanyEdit) -> Company:
        company: Company = await self.repository.get(company_id)
        if not company:
            raise NotFoundException()
        
        if company.id != user.employer.company_id:
            raise NotAllowedException()

        company_data: dict = data.model_dump()
        await self.repository.update_company(company, company_data)

        return company

    async def get_companies(self, start: int, end: int) -> Sequence[Company | None]:
        data = await self.repository.get_many(start ,end)
        return data

    async def get_companies_by_name(
            self, data: SComaniesReadQuery
    ) -> Sequence[Company | None]:
        data = await self.repository.get_companies_by_name(
            registration_date=data.registration_date,
            only_verified=data.only_verified,
            q=data.q,
            start=data.start,
            end=data.end,
            desc=data.desc
        )
        return data
    
    async def count_companies_by_name(
            self, data: SComaniesFilteredQuery
    ) -> int:
        data = await self.repository.count_companies_by_name(
            registration_date=data.registration_date,
            only_verified=data.only_verified,
            q=data.q
        )
        return data

    async def get_company_by_inn(self, inn: str) -> Company | None:
        data = await self.repository.get_company_by_inn(inn)
        if not data:
            raise NotFoundException()

        return data
    
    async def verify_company_by_id(self, id: int) -> None:
        company: Company = await self.get_by_id(id)
        await self.repository.update_company(company, data={"is_verified": True})

    async def unverify_company_by_id(self, id: int) -> None:
        company: Company = await self.get_by_id(id)
        await self.repository.update_company(company, data={"is_verified": False})
