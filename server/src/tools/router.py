from fastapi import APIRouter, Depends

from src.responses import response_204, openapi_404, openapi_204, openapi_400
from src.deps import (
    get_locations_service, get_institutions_service, get_levels_service
)
from src.core.services.catalog import CatalogService
from src.core.schemas.common import SBaseQueryBody
from src.core.schemas.catalog import SBaseCatalogItemRead, SBaseCatalogRead
from src.auth.roles import SystemRole, RoleManager
from src.users.models import User
from src.tools.schemas import SEduInstitutionCreate, SEduLevelCreate, SLocationCreate

router = APIRouter(prefix='/tools', tags=['Tools'])

current_user = RoleManager(SystemRole.ACTIVE)
current_superuser = RoleManager(SystemRole.SUPERUSER)

@router.get('/locations')
async def get_locations(
    params: SBaseQueryBody = Depends(),
    location_service: CatalogService = Depends(get_locations_service)
) -> SBaseCatalogRead:
    locations = await location_service.search_catalog(params)

    return {'count': len(locations),'items': locations}

@router.get('/locations/{id}', responses={**openapi_404})
async def get_location_by_id(
    id: int,
    location_service: CatalogService = Depends(get_locations_service)
) -> SBaseCatalogItemRead:
    location = await location_service.get_by_id(id)
    return location

@router.post('/locations', responses={**openapi_400})
async def add_location(
    data: SLocationCreate,
    user: User = Depends(current_superuser),
    location_service: CatalogService = Depends(get_locations_service)
) -> SBaseCatalogItemRead:
    location = await location_service.add_item(data.name)
    return location

@router.delete('/locations/{id}', responses={**openapi_204, **openapi_404})
async def delete_location_by_id(
    id: int,
    user: User = Depends(current_superuser),
    location_service: CatalogService = Depends(get_locations_service)
):
    await location_service.delete_by_id(id)
    return response_204

@router.patch('/locations/{id}', responses={**openapi_404, **openapi_400})
async def edit_location_by_id(
    id: int,
    data: SLocationCreate,
    user: User = Depends(current_superuser),
    location_service: CatalogService = Depends(get_locations_service)
) -> SBaseCatalogItemRead:
    location = await location_service.edit_item(id, data.name)
    return location


@router.get('/edu-institutions')
async def get_edu_institutions(
    params: SBaseQueryBody = Depends(),
    inst_service: CatalogService = Depends(get_institutions_service)
) -> SBaseCatalogRead:
    institutions = await inst_service.search_catalog(params)

    return {'count': len(institutions),'items': institutions}

@router.get('/edu-institutions/{id}', responses={**openapi_404})
async def get_edu_institutions_by_id(
    id: int,
    inst_service: CatalogService = Depends(get_institutions_service)
) -> SBaseCatalogItemRead:
    institutions = await inst_service.get_by_id(id)
    return institutions

@router.post('/edu-institutions', responses={**openapi_400})
async def add_edu_institution(
    data: SEduInstitutionCreate,
    user: User = Depends(current_superuser),
    inst_service: CatalogService = Depends(get_institutions_service)
) -> SBaseCatalogItemRead:
    edu_institution = await inst_service.add_item(data.name)
    return edu_institution

@router.delete('/edu-institutions/{id}', responses={**openapi_204, **openapi_404})
async def delete_edu_institution_by_id(
    id: int,
    user: User = Depends(current_superuser),
    inst_service: CatalogService = Depends(get_institutions_service)
):
    await inst_service.delete_by_id(id)
    return response_204

@router.patch('/edu-institutions/{id}', responses={**openapi_404, **openapi_400})
async def edit_edu_institution_by_id(
    id: int,
    data: SEduInstitutionCreate,
    user: User = Depends(current_superuser),
    inst_service: CatalogService = Depends(get_institutions_service)
) -> SBaseCatalogItemRead:
    edu_institution = await inst_service.edit_item(id, data.name)
    return edu_institution


@router.get('/edu-levels')
async def get_edu_levels(
    levels_service: CatalogService = Depends(get_levels_service)
) -> SBaseCatalogRead:
    edu_levels = await levels_service.get_all()
    return {'count': len(edu_levels),'items': edu_levels}

@router.post('/edu-levels', responses={**openapi_400})
async def add_edu_level(
    data: SEduLevelCreate,
    user: User = Depends(current_superuser),
    levels_service: CatalogService = Depends(get_levels_service)
) -> SBaseCatalogItemRead:
    edu_level = await levels_service.add_item(data.name)
    return edu_level

@router.delete('/edu-levels/{id}', responses={**openapi_204, **openapi_404})
async def delete_edu_level_by_id(
    id: int,
    user: User = Depends(current_superuser),
    levels_service: CatalogService = Depends(get_levels_service)
):
    await levels_service.delete_by_id(id)
    return response_204

@router.patch('/edu-levels/{id}', responses={**openapi_404, **openapi_400})
async def edit_edu_level_by_id(
    id: int,
    data: SEduLevelCreate,
    user: User = Depends(current_superuser),
    levels_service: CatalogService = Depends(get_levels_service)
) -> SBaseCatalogItemRead:
    edu_level = await levels_service.edit_item(id, data.name)
    return edu_level
