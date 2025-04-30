from typing import Sequence

from src.core.services.common import CommonService
from src.core.repositories.user import UserRepository
from src.core.schemas.common import SBaseQueryBody
from src.exceptions import NotFoundException
from src.users.models import User
from src.users.schemas import SUserEdit


class UserService(CommonService[UserRepository]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(user_repo)

    async def refresh_fields(self, user: User) -> None:
        await self.repository.refresh_fields(user)

    async def update_user(self, user: User, data: SUserEdit) -> None:
        user_data: dict = data.model_dump()
        applicant_data: dict = user_data.pop('applicant', None)

        await self.repository.update_user(user, user_data)

        if applicant_data and user.is_applicant:
            if data.applicant.edu_status:
                applicant_data['edu_status'] = data.applicant.edu_status.value

            await self.repository.update_applicant(user, applicant_data)

    async def get_users(self, start: int, end: int) -> Sequence[User | None]:
        data = await self.repository.get_users_by_fullname(start ,end)
        return data
    
    async def get_users_by_fullname(
            self, data: SBaseQueryBody
    ) -> Sequence[User | None]:
        data = await self.repository.get_users_by_fullname(data.start, data.end, data.q)
        return data
    
    async def get_applicants_by_fullname(
            self, user: User, data: SBaseQueryBody
    ) -> Sequence[User | None]:
        data = await self.repository.get_applicants_by_fullname(
            user, data.start, data.end, data.q
        )
        return data
    
    async def verify_user_by_id(self, id: int) -> None:
        user: User = await self.get_by_id(id)
        await self.repository.update_user(user, data={"is_verified": True})

    async def unverify_user_by_id(self, id: int) -> None:
        user: User = await self.get_by_id(id)
        await self.repository.update_user(user, data={"is_verified": False})

    async def activate_user_by_id(self, id: int) -> None:
        user: User = await self.get_by_id(id)
        await self.repository.update_user(user, data={"is_active": True})

    async def deactivate_user_by_id(self, id: int) -> None:
        user: User = await self.get_by_id(id)
        await self.repository.update_user(user, data={"is_active": False})
