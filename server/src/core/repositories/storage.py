from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.common import CommonRepository
from src.recommendations.models import ProofDocument


class StorageRepository(CommonRepository[ProofDocument]):
    def __init__(self, session: AsyncSession):
        super().__init__(ProofDocument, session)

    async def register_files(self, files_metadata: list[dict]) -> list[ProofDocument]:
        registered = []

        for metadata in files_metadata:
           registered.append(await self._register_file(metadata))

        return registered

    async def register_file(self, file_metadata: dict) -> ProofDocument:
        """Create ProofDocument object (without DB write)"""
        return self.model(**file_metadata)
