from fastapi import APIRouter, Depends, Body

from src.deps import get_neg_service
from src.responses import openapi_401, openapi_400, response_204
from src.core.services.negotiation import NegotiationService
from src.core.schemas.common import SBaseQueryCountResponse
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.negotiations.models import Negotiation, NegotiationStatus
from src.negotiations.schemas import (
    SNegotiationResult, SNegotiationsFilter, SNegotiationAppPreviews,
    SNegotiationEmpPreviews, SNegotiationChangeStatus, SNegotiationsIdBody
)

router = APIRouter(prefix='/negotiations', tags=['Negotiations'])

current_user = RoleManager(SystemRole.ACTIVE)
current_applicant = RoleManager(SystemRole.ACTIVE, SystemRole.VERIFIED, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.ACTIVE,  SystemRole.VERIFIED, SystemRole.EMPLOYER)

@router.get('/applicant')
async def get_applicant_negotiations_cards(
        data: SNegotiationsFilter = Depends(),
        user: User = Depends(current_applicant),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationAppPreviews:
    negotiations = await service.get_negotiations_applicant(
        user.id, data.start, data.end, data.status
    )

    return {'count': len(negotiations), 'items': negotiations}

@router.get('/applicant/count')
async def get_applicant_negotiations_count(
        status: NegotiationStatus = None,
        user: User = Depends(current_applicant),
        service: NegotiationService = Depends(get_neg_service)
) -> SBaseQueryCountResponse:
    count = await service.count_negotiations_applicant(user.id, status)
    return {'count': count}

@router.get('/employer')
async def get_employer_negotiations_cards(
        data: SNegotiationsFilter = Depends(),
        user: User = Depends(current_employer),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationEmpPreviews:
    negotiations = await service.get_negotiations_employer(
        user.id, data.start, data.end, data.status
    )

    return {'count': len(negotiations), 'items': negotiations}

@router.get('/employer/count')
async def get_employer_negotiations_count(
        status: NegotiationStatus = None,
        user: User = Depends(current_employer),
        service: NegotiationService = Depends(get_neg_service)
) -> SBaseQueryCountResponse:
    count = await service.count_negotiations_employer(user.id, status)
    return {'count': count}

@router.post('/employer/accept')
async def accept_negotiation(
        data: SNegotiationChangeStatus,
        user: User = Depends(current_employer),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationResult:
    negotiation: Negotiation = await service.update_negotiation(
        data.negotiation_id,
        user.id,
        NegotiationStatus.ACCEPTED,
        data.employer_description
    )

    return negotiation

@router.post('/employer/reject')
async def reject_negotiation(
        data: SNegotiationChangeStatus,
        user: User = Depends(current_employer),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationResult:
    negotiation: Negotiation = await service.update_negotiation(
        data.negotiation_id,
        user.id,
        NegotiationStatus.REJECTED,
        data.employer_description
    )

    return negotiation

@router.post('/employer/reset')
async def reset_negotiation(
        data: SNegotiationsIdBody,
        user: User = Depends(current_employer),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationResult:
    negotiation: Negotiation = await service.update_negotiation(
        data.negotiation_id, user.id, NegotiationStatus.PENDING, None
    )

    return negotiation

@router.post('/applicant', responses={**openapi_400})
async def create_negotiation(
        vacancy_id: int,
        user: User = Depends(current_applicant),
        service: NegotiationService = Depends(get_neg_service)
) -> SNegotiationResult:
    negotiation = await service.create_negotiation(vacancy_id, user.id)
    return negotiation

@router.delete('/{id}', responses={**openapi_400})
async def delete_negotiation(
        id: int,
        user: User = Depends(current_applicant),
        service: NegotiationService = Depends(get_neg_service)
):
    await service.delete_by_id(id)
    return response_204
