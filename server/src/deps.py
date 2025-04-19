from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.core.repositories.user import UserRepository
from src.core.services.user import UserService
from src.core.repositories.company import CompanyRepository
from src.core.services.company import CompanyService

async def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

async def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


async def get_company_repo(session: AsyncSession = Depends(get_async_session)) -> CompanyRepository:
    return CompanyRepository(session)

async def get_company_service(repo: CompanyRepository = Depends(get_company_repo)) -> CompanyService:
    return CompanyService(repo)
