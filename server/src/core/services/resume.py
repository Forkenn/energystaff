from src.exceptions import NotFoundException, NotAllowedException, AlreadyExistException
from src.core.services.common import CommonService
from src.core.repositories.resume import ResumeRepository
from src.users.models import User
from src.resume.models import Resume
from src.resume.schemas import SResumeCreate


class ResumeService(CommonService[ResumeRepository]):
    def __init__(self, resume_repo: ResumeRepository):
        super().__init__(resume_repo)

    async def get_full_resume(self, id: int) -> Resume:
        vacancy = await self.repository.get_full(id)
        if not vacancy:
            raise NotFoundException()

        return vacancy

    async def get_full_resume_by_uid(self, uid: int) -> Resume:
        resume = await self.repository.get_full_by_uid(uid)
        if not resume:
            raise NotFoundException()

        return resume
    
    async def get_full_resume_by_uid_secured(
            self, requester_id: int, uid: int, include_user: bool = False
    ) -> Resume:
        resume = await self.repository.get_resume_by_uid_secured(
            requester_id, uid, include_user
        )
        if not resume:
            raise NotFoundException()

        return resume

    async def create_resume(self, uid: int, data: SResumeCreate):
        if self.repository.exists_by_uid(uid):
            raise AlreadyExistException()

        data_dict = data.model_dump()
        data_dict['user_id'] = uid
        resume_types_ids = data_dict.pop('resume_types_ids', [])
        resume_formats_ids = data_dict.pop('resume_formats_ids', [])
        new_resume = await self.repository.create(
            data_dict,
            resume_types_ids,
            resume_formats_ids
        )

        return new_resume

    async def update_resume(
            self,
            uid: int,
            data: SResumeCreate
    ) -> Resume:
        resume: Resume = await self.repository.get_full_by_uid(uid)
        if not resume:
            raise NotFoundException()

        resume_data: dict = data.model_dump()
        resume_types_ids = resume_data.pop('resume_types_ids', [])
        resume_formats_ids = resume_data.pop('resume_formats_ids', [])
        await self.repository.update(
            resume,
            resume_data,
            resume_types_ids,
            resume_formats_ids
        )
        return resume

    async def delete_by_uid(self, uid: int) -> None:
        resume: Resume = await self.repository.get_by_uid(uid)
        if not resume:
            raise NotFoundException()

        await self.repository.delete_object(resume)
