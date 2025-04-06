from fastapi import APIRouter, Depends

from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.users.schemas import SUserReadFull

router = APIRouter(prefix='/users', tags=['Users'])

current_user = RoleManager(SystemRole.ACTIVE)

@router.get('/me')
async def get_current_user(
        user: User = Depends(current_user)
) -> SUserReadFull:
    return user
