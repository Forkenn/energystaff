from fastapi import APIRouter, Depends

import sqlalchemy as alch
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import response_204, openapi_404, openapi_204, openapi_400
from src.exceptions import NotFoundException, AlreadyExistException
from src.schemas import SBaseCatalogItemRead, SBaseCatalogRead
from src.dao.common import search_catalog_multi, fetch_one
from src.auth.manager import fastapi_users
from src.users.models import User
from src.tools.models import Location, EduInstitution, EduLevel
from src.tools.schemas import (
    SBaseToolsSearch, SEduInstitutionCreate, SEduLevelCreate, SLocationCreate
)

router = APIRouter(prefix='/tools', tags=['Tools'])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)

@router.get('/locations')
async def get_locations(
    params: SBaseToolsSearch = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> SBaseCatalogRead:
    locations = await search_catalog_multi(
        session, Location, params.q, params.start, params.end
    )

    return {'count': len(locations),'items': locations}

@router.get('/locations/{id}', responses={**openapi_404})
async def get_location_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> SBaseCatalogItemRead:
    location = await session.get(Location, id)
    if not location:
        raise NotFoundException()

    return location

@router.post('/locations', responses={**openapi_400})
async def add_location(
    data: SLocationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    location = await fetch_one(session, Location, Location.name == data.name)
    if location:
        raise AlreadyExistException()

    location = Location(name=data.name)
    session.add(location)
    await session.commit()
    return location

@router.delete('/locations/{id}', responses={**openapi_204, **openapi_404})
async def delete_location_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    location = await session.get(Location, id)
    if not location:
        raise NotFoundException()

    await session.delete(location)
    await session.commit()
    return response_204

@router.patch('/locations/{id}', responses={**openapi_404, **openapi_400})
async def edit_location_by_id(
    id: int,
    data: SLocationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    location = await fetch_one(session, Location, Location.name == data.name)
    if location:
        raise AlreadyExistException()

    location = await session.get(Location, id)
    if not location:
        raise NotFoundException()

    location.name = data.name
    await session.commit()
    return location

@router.get('/edu-institutions')
async def get_edu_institutions(
    params: SBaseToolsSearch = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> SBaseCatalogRead:
    response = await search_catalog_multi(
        session, EduInstitution, params.q, params.start, params.end
    )

    return {'count': len(response),'items': response}

@router.get('/edu-institutions/{id}', responses={**openapi_404})
async def get_edu_institutions_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> SBaseCatalogItemRead:
    response = await session.get(EduInstitution, id)
    if not response:
        raise NotFoundException()

    return response

@router.post('/edu-institutions', responses={**openapi_400})
async def add_edu_institution(
    data: SEduInstitutionCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    edu_institution = await fetch_one(
        session, EduInstitution, EduInstitution.name == data.name
    )
    if edu_institution:
        raise AlreadyExistException()

    edu_institution = EduInstitution(name=data.name)
    session.add(edu_institution)
    await session.commit()
    return edu_institution

@router.delete('/edu-institutions/{id}', responses={**openapi_204, **openapi_404})
async def delete_edu_institution_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    edu_institution = await session.get(EduInstitution, id)
    if not edu_institution:
        raise NotFoundException()

    await session.delete(edu_institution)
    await session.commit()
    return response_204

@router.patch('/edu-institutions/{id}', responses={**openapi_404, **openapi_400})
async def edit_edu_institution_by_id(
    id: int,
    data: SEduInstitutionCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    edu_institution = await fetch_one(
        session, EduInstitution, EduInstitution.name == data.name
    )
    if edu_institution:
        raise AlreadyExistException()

    edu_institution = await session.get(EduInstitution, id)
    if not edu_institution:
        raise NotFoundException()

    edu_institution.name = data.name
    await session.commit()
    return edu_institution

@router.get('/edu-levels')
async def get_edu_levels(
    session: AsyncSession = Depends(get_async_session)
) -> SBaseCatalogRead:
    edu_levels = await search_catalog_multi(
        session, EduLevel
    )
    return {'count': len(edu_levels),'items': edu_levels}

@router.post('/edu-levels', responses={**openapi_400})
async def add_edu_level(
    data: SEduLevelCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    edu_level = await fetch_one(session, EduLevel, EduLevel.name == data.name)
    if edu_level:
        raise AlreadyExistException()

    edu_level = EduLevel(name=data.name)
    session.add(edu_level)
    await session.commit()
    return edu_level

@router.delete('/edu-levels/{id}', responses={**openapi_204, **openapi_404})
async def delete_edu_level_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    edu_level = await session.get(EduLevel, id)
    if not edu_level:
        raise NotFoundException()

    await session.delete(edu_level)
    await session.commit()
    return response_204

@router.patch('/edu-levels/{id}', responses={**openapi_404, **openapi_400})
async def edit_edu_level_by_id(
    id: int,
    data: SEduLevelCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseCatalogItemRead:
    edu_level = await fetch_one(session, EduLevel, EduLevel.name == data.name)
    if edu_level:
        raise AlreadyExistException()

    edu_level = await session.get(EduLevel, id)
    if not edu_level:
        raise NotFoundException()

    edu_level.name = data.name
    await session.commit()
    return edu_level
