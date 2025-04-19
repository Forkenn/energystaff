from typing import Sequence

from src.exceptions import NotFoundException, NotAllowedException
from src.core.services.common import CommonService
from src.core.repositories.company import CompanyRepository
from src.core.schemas.common import SBaseQueryBody
from src.users.models import User
from src.companies.models import Company
from src.companies.schemas import SCompanyEdit


class CompanyService(CommonService[CompanyRepository]):
    def __init__(self, company_repo: CompanyRepository):
        super().__init__(company_repo)

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

    async def search_companies_by_name(
            self, data: SBaseQueryBody
    ) -> Sequence[Company | None]:
        data = await self.repository.get_companies_by_name(data.q, data.start, data.end)
        return data

    async def get_company_by_inn(self, inn: str) -> Company | None:
        data = await self.repository.get_company_by_inn(inn)
        if not data:
            raise NotFoundException()

        return data
