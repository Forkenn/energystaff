from typing import Sequence

from src.exceptions import NotFoundException, NotAllowedException
from src.core.services.common import CommonService
from src.core.repositories.vacancy import VacancyRepository
from src.users.models import User
from src.vacancies.models import Vacancy
from src.vacancies.schemas import (
    SVacancyCreate, SVacanciesCountQuery, SVacanciesPreviewsQuery, SortBy
)


class VacancyService(CommonService[VacancyRepository]):
    def __init__(self, vacancy_repo: VacancyRepository):
        super().__init__(vacancy_repo)

    async def get_full_vacancy(self, id) -> Vacancy:
        vacancy = await self.repository.get_full(id)
        if not vacancy:
            raise NotFoundException()

        return vacancy
    
    async def create_vacancy(self, user: User, data: SVacancyCreate):
        data_dict = data.model_dump()
        data_dict['company_id'] = user.employer.company_id
        data_dict['author_id'] = user.id
        vacancy_types_ids = data_dict.pop('vacancy_types_ids', [])
        vacancy_formats_ids = data_dict.pop('vacancy_formats_ids', [])
        vacancy_schedules_ids = data_dict.pop('vacancy_schedules_ids', [])
        new_vacancy = await self.repository.create(
            data_dict,
            vacancy_schedules_ids,
            vacancy_types_ids,
            vacancy_formats_ids
        )
        return new_vacancy

    async def update_vacancy(
            self,
            requester_id: int,
            vacancy_id: int,
            data: SVacancyCreate
    ) -> Vacancy:
        vacancy: Vacancy = await self.repository.get_full(vacancy_id)
        if not vacancy:
            raise NotFoundException()
        
        if vacancy.author_id != requester_id:
            raise NotAllowedException()

        vacancy_data: dict = data.model_dump()
        vacancy_types_ids = vacancy_data.pop('vacancy_types_ids', [])
        vacancy_formats_ids = vacancy_data.pop('vacancy_formats_ids', [])
        vacancy_schedules_ids = vacancy_data.pop('vacancy_schedules_ids', [])
        await self.repository.update(
            vacancy,
            vacancy_data,
            vacancy_schedules_ids,
            vacancy_types_ids,
            vacancy_formats_ids
        )
        return vacancy

    async def get_vacancies_cards(
            self,
            requester_id: int,
            query_data: SVacanciesPreviewsQuery
        ) -> Sequence[dict | None]:
        data = await self.repository.get_vacancies_plain(
            requester_id=requester_id,
            q=query_data.q,
            location_id=query_data.location_id,
            salary_from=query_data.salary_from,
            salary_to=query_data.salary_to,
            formats_ids=query_data.employment_formats_ids,
            schedules_ids=query_data.employment_schedules_ids,
            types_ids=query_data.employment_types_ids,
            sort_date=True if query_data.sort_by == SortBy.DATE else False,
            desc=query_data.desc,
            start=query_data.start,
            end=query_data.end
        )
        return data
    
    async def count_vacancies(self, query_data: SVacanciesCountQuery) -> int:
        return await self.repository.count_vacancies(
            q=query_data.q,
            location_id=query_data.location_id,
            salary_from=query_data.salary_from,
            salary_to=query_data.salary_to,
            formats_ids=query_data.employment_formats_ids,
            schedules_ids=query_data.employment_schedules_ids,
            types_ids=query_data.employment_types_ids
        )
    
    async def delete_by_id(self, requester_id: int, id: int) -> None:
        vacancy: Vacancy = await self.get_by_id(id)

        if vacancy.author_id != requester_id:
            raise NotAllowedException()

        await self.repository.delete_object(vacancy)

    async def force_delete_by_id(self, id: int) -> None:
        vacancy: Vacancy = await self.get_by_id(id)

        await self.repository.delete_object(vacancy)
