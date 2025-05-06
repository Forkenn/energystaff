from typing import Sequence

from src.core.services.common import CommonService
from src.core.repositories.user import UserRepository
from src.exceptions import NotFoundException
from src.users.models import User
from src.users.schemas import (
    SUserEdit, SApplicantsReadQuery, SUsersReadQuery, SUsersFilteredQuery,
)


class UserService(CommonService[UserRepository]):
    def __init__(self, user_repo: UserRepository):
        super().__init__(user_repo)

    async def create_applicant(self, user: User) -> None:
        await self.repository.create_applicant(user)

    async def create_employer(self, user: User, company_id: int) -> None:
        await self.repository.create_employer(user, company_id)

    async def create_edu_worker(self, user: User, edu_institution_id: int) -> None:
        await self.repository.create_edu_worker(user, edu_institution_id)

    async def get_full_by_id(self, id: int) -> User:
        user = await self.repository.get(id)
        await self.repository.refresh_fields(user)
        return user

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
            self, data: SUsersReadQuery
    ) -> Sequence[User | None]:
        data = await self.repository.get_users_by_fullname(
            birthdate=data.birthdate,
            only_verified=data.only_verified,
            location_id=data.location_id,
            q=data.q,
            start=data.start,
            end=data.end,
            desc=data.desc
        )
        return data
    
    async def count_users_by_fullname(
            self, data: SUsersFilteredQuery
    ) -> int:
        data = await self.repository.count_users_by_fullname(
            birthdate=data.birthdate,
            only_verified=data.only_verified,
            location_id=data.location_id,
            q=data.q
        )

        return data
    
    async def get_applicant_by_id(self, user: User, id: int) -> User:
        data = await self.repository.get_applicant_by_id(
            edu_institution_id=user.edu_worker.edu_institution_id,
            id=id
        )
        if not data:
            raise NotFoundException()

        return data
    
    async def get_applicant_by_edu_num(self, user: User, edu_number: int) -> User:
        data = await self.repository.get_applicant_by_edu_num(
            edu_institution_id=user.edu_worker.edu_institution_id,
            edu_number=edu_number
        )
        if not data:
            raise NotFoundException()

        return data
    
    async def get_applicants_by_fullname(
            self, user: User, data: SApplicantsReadQuery
    ) -> Sequence[User | None]:
        data = await self.repository.get_applicants_by_fullname(
            edu_institution_id=user.edu_worker.edu_institution_id,
            birthdate=data.birthdate,
            only_verified=data.only_verified,
            location_id=data.location_id,
            q=data.q, start=data.start, end=data.end
        )
        return data

    async def count_applicants_by_fullname(
            self, user: User, data: SApplicantsReadQuery
    ) -> int:
        data = await self.repository.count_applicants_by_fullname(
            edu_institution_id=user.edu_worker.edu_institution_id,
            birthdate=data.birthdate,
            only_verified=data.only_verified,
            location_id=data.location_id,
            q=data.q
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
