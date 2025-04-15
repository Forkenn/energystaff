from typing import Annotated
from pydantic import BaseModel, Field

from src.core.schemas.catalog import SBaseCatalogItemRead


class SResumeCreate(BaseModel):
    position: str = Field(
        default=...,
        min_length=5,
        max_length=120,
        description="Position from 5 to 120 symbols"
    )
    specialization: str = Field(
        default=...,
        min_length=5,
        max_length=120,
        description="Specialization from 5 to 120 symbols"
    )
    salary: int = Field(None, ge=0)
    description: str = Field(
        default=...,
        min_length=0,
        max_length=500,
        description="Description from 0 to 500 symbols"
    )
    resume_types_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    resume_formats_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)


class SResumeRead(BaseModel):
    id: int
    position: str
    specialization: str
    salary: int
    description: str
    resume_types: list[SBaseCatalogItemRead]
    resume_formats: list[SBaseCatalogItemRead]
