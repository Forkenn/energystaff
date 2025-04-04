from fastapi import APIRouter, Depends

import sqlalchemy as alch
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.responses import response_204, openapi_404, openapi_204, openapi_400
from src.exceptions import NotFoundException, AlreadyExistException
from src.auth.manager import fastapi_users
from src.users.models import User
from src.tools.models import Location, EduInstitution, EduLevel
from src.tools.schemas import (
    SBaseToolsRead, SBaseToolRead, SBaseToolsSearch, SEduInstitutionCreate,
    SEduLevelCreate, SLocationCreate
)

router = APIRouter(prefix='/tools', tags=['Tools'])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)

@router.get('/locations')
async def get_locations(
    params: SBaseToolsSearch = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> SBaseToolsRead:
    query = alch.select(Location)
    if params.q:
        query = query.where(Location.name.like(f'{params.q}%'))
    if params.start and params.end:
        query = query.slice(params.start, params.end)

    locations = (await session.execute(query)).scalars().all()
    return {'count': len(locations),'items': locations}

@router.get('/locations/{id}', responses={**openapi_404})
async def get_location_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> SBaseToolRead:
    location = await session.get(Location, id)
    if not location:
        raise NotFoundException()

    return location

@router.post('/locations', responses={**openapi_400})
async def add_location(
    data: SLocationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseToolRead:
    query = alch.select(Location).where(Location.name == data.name)
    location = (await session.execute(query)).scalar()
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
) -> SBaseToolRead:
    query = alch.select(Location).where(Location.name == data.name)
    location = (await session.execute(query)).scalar()
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
) -> SBaseToolsRead:
    query = alch.select(EduInstitution)
    if params.q:
        query = query.where(EduInstitution.name.like(f'%{params.q}%'))
    if params.start and params.end:
        query = query.slice(params.start, params.end)

    response = (await session.execute(query)).scalars().all()
    return {'count': len(response),'items': response}

@router.get('/edu-institutions/{id}', responses={**openapi_404})
async def get_edu_institutions_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
) -> SBaseToolRead:
    response = await session.get(EduInstitution, id)
    if not response:
        raise NotFoundException()

    return response

@router.post('/edu-institutions', responses={**openapi_400})
async def add_edu_institution(
    data: SEduInstitutionCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseToolRead:
    query = alch.select(EduInstitution).where(EduInstitution.name == data.name)
    edu_institution = (await session.execute(query)).scalar()
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
) -> SBaseToolRead:
    query = alch.select(EduInstitution).where(EduInstitution.name == data.name)
    edu_institution = (await session.execute(query)).scalar()
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
) -> SBaseToolsRead:
    query = alch.select(EduLevel)
    edu_levels = (await session.execute(query)).scalars().all()
    return {'count': len(edu_levels),'items': edu_levels}

@router.post('/edu-levels', responses={**openapi_400})
async def add_edu_level(
    data: SEduLevelCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
) -> SBaseToolRead:
    query = alch.select(EduLevel).where(EduLevel.name == data.name)
    edu_level = (await session.execute(query)).scalar()
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
) -> SBaseToolRead:
    query = alch.select(EduLevel).where(EduLevel.name == data.name)
    edu_level = (await session.execute(query)).scalar()
    if edu_level:
        raise AlreadyExistException()

    edu_level = await session.get(EduLevel, id)
    if not edu_level:
        raise NotFoundException()

    edu_level.name = data.name
    await session.commit()
    return edu_level
