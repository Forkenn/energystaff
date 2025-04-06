from enum import Enum

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import ForbiddenException
from src.auth.manager import fastapi_users
from src.users.models import User

current_user = fastapi_users.current_user()


class SystemRole(Enum):
    ACTIVE = 'is_active'
    SUPERUSER = 'is_superuser'
    VERIFIED = 'is_verified'
    APPLICANT = 'is_applicant'
    EMPLOYER = 'is_employer'
    EDU_WORKER = 'is_edu'


class RoleManager:
    def __init__(self, *required_roles: SystemRole):
        self.required_roles = required_roles

    async def __call__(
            self,
            user: User = Depends(current_user),
            session: AsyncSession = Depends(get_async_session)
    ):
        roles_mapping = {
            SystemRole.ACTIVE: user.is_active,
            SystemRole.SUPERUSER: user.is_superuser,
            SystemRole.VERIFIED: user.is_verified,
            SystemRole.APPLICANT: user.is_applicant,
            SystemRole.EMPLOYER: user.is_employer,
            SystemRole.EDU_WORKER: user.is_edu
        }

        missing_roles = [
            role for role in self.required_roles if not roles_mapping.get(role, False)
        ]

        print(missing_roles)

        if missing_roles:
            raise ForbiddenException()
        
        await session.refresh(user, ('applicant', 'employer', 'edu_worker'))
        return user

