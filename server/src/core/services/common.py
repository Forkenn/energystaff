import sqlalchemy as alch

from typing import TypeVar, Generic, Type, Sequence

from src.exceptions import NotFoundException
from src.core.repositories.common import CommonRepository
from src.core.schemas.common import SBaseQuerySliceBody

R = TypeVar('R', bound=CommonRepository)


class CommonService(Generic[R]):
    def __init__(self, repository: Type[R]):
        self.repository = repository

    async def get_by_id(self, id: int):
        result = await self.repository.get(id)
        if not result:
            raise NotFoundException()
        
        return result
    
    async def get_all_sliced(self, slice: SBaseQuerySliceBody) -> Sequence:
        result = await self.repository.get_many(slice.start, slice.end)
        return result
    
    async def delete_by_id(self, id: int):
        await self.repository.delete(id)
