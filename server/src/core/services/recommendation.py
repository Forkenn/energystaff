from src.exceptions import NotFoundException, ForbiddenException, AlreadyExistException
from src.core.services.common import CommonService
from src.core.repositories.recommendation import RecommendationRepository
from src.core.services.storage import StorageService
from src.core.dto.file import FileDTO
from src.users.models import User, EduWorker
from src.recommendations.models import Recommendation
from src.recommendations.schemas import (
    SRecommendationCreate, SRecommendationUpdate
)

DOCUMENTS_PATH = 'proof_documents'


class RecommendationService(CommonService[RecommendationRepository]):
    def __init__(
            self,
            recommendation_repo: RecommendationRepository,
            storage_service: StorageService
    ):
        self.storage = storage_service
        super().__init__(recommendation_repo)

    async def get_by_uid(self, uid: int) -> Recommendation:
        recommendation = await self.repository.get_by_uid(uid)
        if not recommendation:
            raise NotFoundException()

        return recommendation
    
    async def get_full_by_uid(self, uid: int) -> Recommendation:
        recommendation = await self.repository.get_full_by_uid(uid)
        if not recommendation:
            raise NotFoundException()

        return recommendation
    
    async def get_full_by_uid_secured(
            self, requester: User, uid: int
    ) -> Recommendation:
        if (
            requester.is_employer or
            requester.is_superuser or
            (requester.is_applicant and requester.id == uid)
        ):
            recommendation = await self.repository.get_full_by_uid(uid)

        elif requester.is_edu:
            recommendation = await self.repository.get_full_by_uid_secured_edu(
                uid, requester.edu_worker.edu_institution_id
            )

        else:
            raise ForbiddenException()

        if not recommendation:
            raise NotFoundException()

        return recommendation

    async def create_recommendation(
            self, uid: int, documents: list[FileDTO], data: SRecommendationCreate
    ) -> Recommendation:
        if await self.repository.exists_by_uid(uid):
            raise AlreadyExistException()
        
        documents_objects = await self.storage.upload_files(
            DOCUMENTS_PATH, documents
        )

        data_dict = data.model_dump()
        data_dict['applicant_id'] = uid
        recommendation = await self.repository.create(documents_objects, data_dict)

        return recommendation

    async def update_recommendation(
            self,
            id: int,
            requester: EduWorker,
            data: SRecommendationUpdate,
            documents: list[FileDTO] = None
    ) -> Recommendation:
        recommendation: Recommendation = await self.repository.get_full_secured(
            id, requester.edu_institution_id
        )
        if not recommendation:
            raise NotFoundException()

        recommendation_data: dict = data.model_dump()
        deleted_documents: list = recommendation_data.pop('deleted_documents', None)

        if deleted_documents:
            await self.storage.delete_files(DOCUMENTS_PATH, deleted_documents)

            recommendation.documents = [
                document for document in recommendation.documents 
                    if document.real_name not in deleted_documents
            ]

        if documents:
            recommendation.documents.extend(
                await self.storage.upload_files(DOCUMENTS_PATH, documents)
            )

        await self.repository.update(
            recommendation,
            recommendation_data
        )

        return recommendation
    
    async def delete_by_id(self, id: int):
        recommendation: Recommendation = await self.repository.get_full(id)
        if not recommendation:
            raise NotFoundException()

        deleted_documents = [
            document.real_name for document in recommendation.documents
        ]
        await self.storage.delete_files(DOCUMENTS_PATH, deleted_documents)
        await self.repository.delete_object(recommendation)

    async def delete_by_uid(self, uid: int) -> None:
        recommendation: Recommendation = await self.repository.get_by_uid(uid)
        if not recommendation:
            raise NotFoundException()
        
        deleted_documents = [
            document.real_name for document in recommendation.documents
        ]
        await self.storage.delete_files(DOCUMENTS_PATH, deleted_documents)
        await self.repository.delete_object(recommendation)
