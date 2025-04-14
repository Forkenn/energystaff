from fastapi import APIRouter, Depends, Body

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import openapi_401, openapi_400, response_204
from src.exceptions import (
    NotFoundException, AlreadyExistException, WrongStateException,
    NotAllowedException
)
from src.core.dao.common import fetch_one
from src.core.dao.negotiations import (
    fetch_negotiations_applicant, count_negotiations_applicant,
    fetch_negotiations_employer, count_negotiations_employer,
    set_negotiation_status
)
from src.core.schemas.common import SBaseQueryCountResponse
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.vacancies.models import Vacancy
from src.negotiations.models import Negotiation, NegotiationStatus
from src.negotiations.schemas import (
    SNegotiationResult, SNegotiationsFilter, SNegotiationAppPreviews,
    SNegotiationEmpPreviews, SNegotiationChangeStatus, SNegotiationsIdBody
)

router = APIRouter(prefix='/negotiations', tags=['Negotiations'])

current_user = RoleManager(SystemRole.ACTIVE)
current_applicant = RoleManager(SystemRole.ACTIVE, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.ACTIVE, SystemRole.EMPLOYER)

@router.get('/applicant')
async def get_applicant_negotiations_cards(
        data: SNegotiationsFilter = Depends(),
        user: User = Depends(current_applicant),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationAppPreviews:
    negotiations = await fetch_negotiations_applicant(
        session, user.id, data.start, data.end, data.status
    )

    return {'count': len(negotiations), 'items': negotiations}

@router.get('/applicant/count')
async def get_applicant_negotiations_count(
        status: NegotiationStatus = None,
        user: User = Depends(current_applicant),
        session: AsyncSession = Depends(get_async_session)
) -> SBaseQueryCountResponse:
    count = await count_negotiations_applicant(
        session, user.id, status
    )

    return {'count': count}

@router.get('/employer')
async def get_employer_negotiations_cards(
        data: SNegotiationsFilter = Depends(),
        user: User = Depends(current_employer),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationEmpPreviews:
    negotiations = await fetch_negotiations_employer(
        session, user.id, data.start, data.end, data.status
    )

    return {'count': len(negotiations), 'items': negotiations}

@router.get('/employer/count')
async def get_employer_negotiations_count(
        status: NegotiationStatus = None,
        user: User = Depends(current_employer),
        session: AsyncSession = Depends(get_async_session)
) -> SBaseQueryCountResponse:
    count = await count_negotiations_employer(
        session, user.id, status
    )

    return {'count': count}

@router.post('/employer/accept')
async def accept_negotiation(
        data: SNegotiationChangeStatus,
        user: User = Depends(current_employer),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationResult:
    negotiation: Negotiation = await session.get(Negotiation, data.negotiation_id)
    if not negotiation:
        raise NotFoundException()
    
    if negotiation.employer_id != user.id:
        raise NotAllowedException()
    
    await set_negotiation_status(
        session,
        negotiation,
        NegotiationStatus.ACCEPTED.value,
        description=data.desctiption
    )

    return negotiation

@router.post('/employer/reject')
async def reject_negotiation(
        data: SNegotiationChangeStatus,
        user: User = Depends(current_employer),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationResult:
    negotiation: Negotiation = await session.get(Negotiation, data.negotiation_id)
    if not negotiation:
        raise NotFoundException()
    
    if negotiation.employer_id != user.id:
        raise NotAllowedException()
    
    await set_negotiation_status(
        session, negotiation, NegotiationStatus.REJECTED.value
    )

    return negotiation

@router.post('/employer/reset')
async def reset_negotiation(
        data: SNegotiationsIdBody,
        user: User = Depends(current_employer),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationResult:
    negotiation: Negotiation = await session.get(Negotiation, data.negotiation_id)
    if not negotiation:
        raise NotFoundException()
    
    if negotiation.employer_id != user.id:
        raise NotAllowedException()
    
    if negotiation.status not in (
        NegotiationStatus.ACCEPTED.value, NegotiationStatus.REJECTED.value
    ):
        raise WrongStateException()
    
    await set_negotiation_status(
        session, negotiation, NegotiationStatus.PENDING.value
    )

    return negotiation

@router.post('/applicant', responses={**openapi_400})
async def create_negotiation(
        vacancy_id: int,
        user: User = Depends(current_applicant),
        session: AsyncSession = Depends(get_async_session)
) -> SNegotiationResult:
    vacancy: Vacancy = await fetch_one(
        session,
        Vacancy,
        where=(Vacancy.id == vacancy_id,)
    )

    if not vacancy:
        raise NotFoundException()
    
    negotiation: Negotiation = await fetch_one(
        session,
        Negotiation,
        where=(
            Negotiation.vacancy_id == vacancy_id,
            Negotiation.applicant_id == user.id
        )
    )

    if negotiation:
        raise AlreadyExistException()

    negotiation = Negotiation()
    negotiation.applicant = user
    negotiation.vacancy = vacancy
    negotiation.employer_id = vacancy.author_id
    session.add(negotiation)
    await session.commit()
    return negotiation

@router.delete('/{id}', responses={**openapi_400})
async def delete_negotiation(
        id: int,
        user: User = Depends(current_applicant),
        session: AsyncSession = Depends(get_async_session)
):
    negotiation: Negotiation = await fetch_one(
        session,
        Negotiation,
        where=(
            Negotiation.id == id,
            Negotiation.applicant_id == user.id
        )
    )

    if not negotiation:
        raise NotFoundException()
    
    if negotiation.status not in (
        NegotiationStatus.ACCEPTED.value, NegotiationStatus.PENDING.value
    ):
        raise WrongStateException()

    await session.delete(negotiation)
    await session.commit()
    return response_204
