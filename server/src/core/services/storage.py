import os
import string
import random

from pathlib import Path

from src.config import STORAGE_PATH
from src.core.services.common import CommonService
from src.core.repositories.storage import StorageRepository
from src.core.dto.file import FileDTO
from src.recommendations.models import ProofDocument


class StorageService(CommonService[StorageRepository]):
    def __init__(self, storage_repo: StorageRepository):
        super().__init__(storage_repo)

    async def upload_files(self, dir_path: Path, files: list[FileDTO]) -> list[ProofDocument]:
        files_objects = []
        for file_metadata in files:
            files_objects.append(self.upload_file(dir_path, file_metadata))

        return files_objects

    async def upload_file(self, dir_path: Path, file_metadata: FileDTO) -> ProofDocument:
        data = file_metadata.file.read()

        prefix = ''.join(
            random.SystemRandom().choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            ) for _ in range(30)
        )

        file_metadata.real_name = '_'.join((prefix, *file_metadata.filename.split()))

        save_to = STORAGE_PATH / dir_path / file_metadata.real_name
        os.makedirs(os.path.dirname(save_to), exist_ok=True)

        with open(save_to, "wb") as f:
            f.write(data)

        return await self.repository.register_file(FileDTO.to_dict())
    
    async def delete_by_ids(self, ids: list[int]):
        pass

    async def delete_by_id(self, id: int):
        pass
