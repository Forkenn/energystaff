from enum import Enum

from fastapi import Depends

from src.deps import get_user_service
from src.exceptions import ForbiddenException
from src.core.services.user import UserService
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
            user_service: UserService = Depends(get_user_service)
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

        if missing_roles:
            raise ForbiddenException()
        
        await user_service.refresh_fields(user)
        return user
