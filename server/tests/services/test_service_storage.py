import os.path

import pytest

from tempfile import SpooledTemporaryFile
from pathlib import Path

from src.recommendations.models import ProofDocument

from src.core.services.storage import StorageService
from src.core.dto.file import FileDTO

TEST_FILES_PATH = Path('test_documents')


async def file():
    return FileDTO(
        download_name='Test_file',
        size=0,
        file=SpooledTemporaryFile()
    )


@pytest.mark.asyncio
async def test_upload_files(storage_service: StorageService):
    file_1 = await file()
    file_2 = await file()

    documents = await storage_service.upload_files(TEST_FILES_PATH, [file_1, file_2])

    assert len(documents) == 2
    assert documents[0].download_name == 'Test_file'
    assert documents[1].download_name == 'Test_file'
    assert documents[0].real_name is not None
    assert documents[1].real_name is not None
    assert os.path.isfile(f'storage/{TEST_FILES_PATH}/{documents[0].real_name}')
    assert os.path.isfile(f'storage/{TEST_FILES_PATH}/{documents[0].real_name}')


@pytest.mark.asyncio
async def test_upload_file(storage_service: StorageService):
    document = await file()

    document = await storage_service.upload_file(TEST_FILES_PATH, document)

    assert document.download_name == 'Test_file'
    assert document.real_name is not None
    assert os.path.isfile(f'storage/{TEST_FILES_PATH}/{document.real_name}')


@pytest.mark.asyncio
async def test_delete_files(storage_service: StorageService):
    file_1 = await file()
    file_2 = await file()

    documents = await storage_service.upload_files(TEST_FILES_PATH, [file_1, file_2])
    await storage_service.delete_files(TEST_FILES_PATH, [file_1.real_name, file_2.real_name])

    assert not os.path.isfile(f'storage/{TEST_FILES_PATH}/{documents[0].real_name}')
    assert not os.path.isfile(f'storage/{TEST_FILES_PATH}/{documents[0].real_name}')


@pytest.mark.asyncio
async def test_delete_file(storage_service: StorageService):
    document = await file()

    document = await storage_service.upload_file(TEST_FILES_PATH, document)
    await storage_service.delete_file(TEST_FILES_PATH, document.real_name)

    assert not os.path.isfile(f'storage/{TEST_FILES_PATH}/{document.real_name}')
