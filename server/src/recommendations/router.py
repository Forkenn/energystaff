from fastapi import APIRouter, UploadFile, Depends

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.storage import StorageManager
from src.responses import openapi_404, openapi_403, openapi_204, openapi_400, response_204
from src.exceptions import NotFoundException, BadRequestException, NotAllowedException
from src.core.dao.common import fetch_all, fetch_one, object_exists
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User, Applicant
from src.recommendations.models import Recommendation, ProofDocument
from src.recommendations.schemas import (
    SRecommendationRead, SRecommendationCreate, SRecommendationUpdate
)

DOCUMENTS_PATH = 'proof_documents'

router = APIRouter(prefix='/recommendations', tags=['Recommendations'])

current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EMPLOYER)
current_edu = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EDU_WORKER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('')
async def get_recommendation_by_user_id(
        applicant_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_edu)
) -> SRecommendationRead:
    applicant: Applicant = await fetch_one(
        session,
        Applicant,
        where=(
            Applicant.edu_institution_id == user.edu_worker.edu_institution_id,
        )
    )

    if not applicant:
        raise NotAllowedException()
    
    recommendation = await fetch_one(
        session,
        Recommendation,
        where=(
            Recommendation.applicant_id == applicant_id,
        ),
        options=(
            joinedload(Recommendation.documents),
        )
    )

    if not recommendation:
        raise NotFoundException()
    
    return recommendation

@router.post('')
async def add_recommendation(
        applicant_id: int,
        data: SRecommendationCreate,
        documents: list[UploadFile],
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_edu)
) -> SRecommendationRead:
    if not await object_exists(
        session, Applicant.user_id == applicant_id
    ):
        raise NotFoundException()
    
    new_recommendation = Recommendation(
        description=data.description,
        applicant_id=applicant_id
    )

    new_recommendation.documents = await StorageManager.save_files(
        documents, DOCUMENTS_PATH, ProofDocument
    )

    session.add(new_recommendation)
    await session.commit()
    await session.refresh(new_recommendation, ('documents',))
    return new_recommendation

@router.patch('/{id}')
async def edit_recommendation(
        id: int,
        data: SRecommendationUpdate,
        documents: list[UploadFile] = None,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_edu)
) -> SRecommendationRead:
    recommendation = await session.get(Recommendation, id)
    if not recommendation:
        raise NotFoundException()
    
    await session.refresh(recommendation, ('documents',))
    
    deleted_documents = data.deleted_documents
    
    if deleted_documents:
        await StorageManager.delete_files(deleted_documents, DOCUMENTS_PATH)
        recommendation.documents = [
            document for document in recommendation.documents 
                if document.real_name not in deleted_documents
        ]

    if documents:
        recommendation.documents.extend(
            await StorageManager.save_files(documents, DOCUMENTS_PATH, ProofDocument)
        )

    recommendation.description = data.description
    await session.commit()
    return recommendation

@router.delete('/{id}')
async def delete_recommendation(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_edu)
):
    recommendation = await session.get(Recommendation, id)
    if not recommendation:
        raise NotFoundException()
    
    await session.delete(recommendation)
    await session.commit()
    return response_204
