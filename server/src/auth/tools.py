from fastapi import Depends, HTTPException, status, Request, Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import exceptions
from fastapi_users.router.common import ErrorCode
 
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import SUserCreate
from src.database import get_async_session
from src.users.models import User

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def create_user_role(
        request: Request,
        user_create_schema: SUserCreate,
        user_manager,
) -> User:
    try:
        return await user_manager.create(
            user_create_schema, safe=True, request=request
        )
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
