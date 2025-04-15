import os
import random
import logging
import string

from pathlib import Path
from typing import Callable

from fastapi import UploadFile


class StorageManager:
    STORAGE_PATH = Path() / "storage"

    @classmethod
    async def save_files(
            cls,
            files: list[UploadFile],
            dir_path: str,
            model: Callable
    ):
        saved_files = []

        file: UploadFile
        for file in files:
            saved_files.append(model(**(await cls._save(file, cls.STORAGE_PATH / dir_path))))

        return saved_files

    @classmethod
    async def delete_files(cls, filenames: list[str], dir_path: str) -> None:
        for name in filenames:
            await cls._delete(name, cls.STORAGE_PATH / dir_path)

    @staticmethod
    async def _delete(name: str, dir_path: Path) -> None:
        file = dir_path / name
        try:
            file.unlink()
        except FileNotFoundError:
            logging.warning(f"File with name {name} does not exists.")

    @staticmethod
    async def _save(file: UploadFile, dir_path: Path) -> dict:
        data = await file.read()
        random_string = ''.join(
            random.SystemRandom().choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            ) for _ in range(20)
        )
        corrected_file_name = '_'.join((random_string, *file.filename.split()))
        save_to = dir_path / corrected_file_name
        os.makedirs(os.path.dirname(save_to), exist_ok=True)

        with open(save_to, "wb") as f:
            f.write(data)

        return dict(
            download_name=file.filename,
            real_name=corrected_file_name,
            size=file.size
        )
