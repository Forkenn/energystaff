from fastapi import APIRouter, UploadFile, Depends


from src.deps import get_recomm_service
from src.responses import openapi_404, openapi_403, openapi_204, openapi_400, response_204
from src.core.services.recommendation import RecommendationService
from src.core.dto.file import FileDTO
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.recommendations.schemas import (
    SRecommendationRead, SRecommendationCreate, SRecommendationUpdate
)

DOCUMENTS_PATH = 'proof_documents'

router = APIRouter(prefix='/recommendations', tags=['Recommendations'])

current_verified = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE)
current_user = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.APPLICANT)
current_employer = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EMPLOYER)
current_edu = RoleManager(SystemRole.VERIFIED, SystemRole.ACTIVE, SystemRole.EDU_WORKER)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('')
async def get_recommendation_by_user_id(
        applicant_id: int,
        user: User = Depends(current_verified),
        service: RecommendationService = Depends(get_recomm_service)
) -> SRecommendationRead:
    recommendation = await service.get_full_by_uid_secured(user, applicant_id)
    return recommendation

@router.post('')
async def add_recommendation(
        applicant_id: int,
        data: SRecommendationCreate,
        documents: list[UploadFile],
        user: User = Depends(current_edu),
        service: RecommendationService = Depends(get_recomm_service)
) -> SRecommendationRead:
    file: UploadFile = None
    new_documents = [
        FileDTO(
            download_name=file.filename,
            file=file.file,
            size=file.size
        ) for file in documents
    ]

    new_recommendation = await service.create_recommendation(
        applicant_id, new_documents, data
    )
    return new_recommendation

@router.patch('/{id}')
async def edit_recommendation(
        id: int,
        data: SRecommendationUpdate,
        documents: list[UploadFile] = None,
        user: User = Depends(current_edu),
        service: RecommendationService = Depends(get_recomm_service)
) -> SRecommendationRead:
    file: UploadFile = None
    new_documents = None

    if documents:
        new_documents = [
            FileDTO(
                download_name=file.filename,
                file=file.file,
                size=file.size
            ) for file in documents
        ]

    recommendation = await service.update_recommendation(
        id, user.edu_worker, data, new_documents
    )

    return recommendation

@router.delete('/{id}')
async def delete_recommendation(
        id: int,
        user: User = Depends(current_edu),
        service: RecommendationService = Depends(get_recomm_service)
):
    await service.delete_by_id(id)
    return response_204
