from typing import Sequence, TypeVar, Generic

from src.exceptions import NotFoundException, AlreadyExistException
from src.core.services.common import CommonService
from src.core.repositories.catalog import CatalogRepository
from src.core.schemas.common import SBaseQueryBody

T = TypeVar("T")


class CatalogService(CommonService[CatalogRepository], Generic[T]):
    def __init__(self, model: type[T], catalog_repo: CatalogRepository):
        self.model = model
        super().__init__(catalog_repo)

    async def get_all(self) -> Sequence[T | None]:
        return await self.repository.get_all()
    
    async def search_catalog(self, data: SBaseQueryBody) -> Sequence[T | None]:
        return await self.repository.search_catalog(data.q, data.start, data.end)

    async def update_catalog_item(self, id: int) -> T:
        pass

    async def add_item(self, name: str) -> T:
        if await self.repository.exists_by_name(name):
            raise AlreadyExistException()
        
        new_item = await self.repository.create(name)
        return new_item
    
    async def edit_item(self, id: int, name: str):
        if await self.repository.exists_by_name(name):
            raise AlreadyExistException()
        
        item = await self.repository.get(id)

        if not item:
            raise AlreadyExistException()
        
        await self.repository.edit(item, name)
        return item
