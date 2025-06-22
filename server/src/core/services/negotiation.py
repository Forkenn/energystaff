from typing import Sequence

from src.exceptions import (
    NotFoundException, AlreadyExistException, WrongStateException,
    NotAllowedException
)
from src.core.services.common import CommonService
from src.core.repositories.negotiation import NegotiationRepository
from src.core.services.vacancy import VacancyService
from src.vacancies.models import Vacancy
from src.negotiations.models import Negotiation, NegotiationStatus


class NegotiationService(CommonService[NegotiationRepository]):
    def __init__(
            self,
            negotiation_repo: NegotiationRepository,
            vacancy_service: VacancyService
    ):
        self.vacancy_service = vacancy_service
        super().__init__(negotiation_repo)

    async def get_negotiations_applicant(
            self,
            applicant_id: int,
            start: int,
            end: int,
            status: NegotiationStatus = None
    ) -> Sequence[dict]:
        negotiations = await self.repository.get_negotiations_applicant(
            applicant_id, start, end, status
        )

        return negotiations
    
    async def count_negotiations_applicant(
            self, applicant_id: int, status: NegotiationStatus = None
    ) -> int:
        count = await self.repository.count_negotiations_applicant(
            applicant_id, status
        )
        return count
    
    async def get_negotiations_employer(
            self,
            employer_id: int,
            start: int,
            end: int,
            status: NegotiationStatus = None
    ) -> Sequence[dict]:
        negotiations = await self.repository.get_negotiations_employer(
            employer_id, start, end, status
        )

        return negotiations
    
    async def count_negotiations_employer(
            self, employer_id: int, status: NegotiationStatus = None
    ) -> int:
        count = await self.repository.count_negotiations_employer(
            employer_id, status
        )
        return count

    async def create_negotiation(
            self, vacancy_id: int, applicant_id: int
    ) -> Negotiation:
        vacancy: Vacancy = await self.vacancy_service.get_by_id(vacancy_id)
        if not vacancy:
            raise NotFoundException()
        
        if await self.repository.exists_for_applicant(
            vacancy_id, applicant_id
        ):
            raise AlreadyExistException()
        
        negotiation = await self.repository.create(
            applicant_id, vacancy.author_id, vacancy_id
        )
    
        return negotiation

    async def update_negotiation(
            self,
            id: int,
            requester_id: int,
            status: NegotiationStatus,
            description: str = None
    ) -> Negotiation:
        negotiation: Negotiation = await self.repository.get(id)
        if not negotiation:
            raise NotFoundException()

        if negotiation.employer_id != requester_id:
            raise NotAllowedException()
    
        if status == NegotiationStatus.PENDING and negotiation.status not in (
            NegotiationStatus.ACCEPTED.value, NegotiationStatus.REJECTED.value
        ):
            raise WrongStateException()
        
        await self.repository.update(negotiation, status, description)
        return negotiation
    
    async def delete_by_id(self, id) -> None:
        negotiation: Negotiation = await self.repository.get(id)
        if not negotiation:
            raise NotFoundException()
        
        if negotiation.status != NegotiationStatus.PENDING.value:
            raise WrongStateException()

        return await super().delete_by_id(id)
