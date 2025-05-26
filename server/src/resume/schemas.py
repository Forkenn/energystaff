from datetime import date
from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator

from src.core.schemas.catalog import SBaseCatalogItemRead
from src.tools.models import EduStatus
from src.users.schemas import SApplicantRead


class SResumeCreate(BaseModel):
    position: str = Field(
        default=...,
        min_length=4,
        max_length=120,
        description="Position from 4 to 120 symbols"
    )
    specialization: str = Field(
        default=...,
        min_length=4,
        max_length=120,
        description="Specialization from 4 to 120 symbols"
    )
    salary: int | None = Field(..., ge=0, le=5000000)
    description: str | None = Field(
        default=...,
        min_length=0,
        max_length=5000,
        description="Description from 0 to 5000 symbols"
    )
    resume_types_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)
    resume_formats_ids: list[Annotated[int, Field(strict=True, ge=0)]] = Field(..., min_length=1)

    @field_validator("salary", mode="before")
    @classmethod
    def set_default_if_none(cls, v):
        return v if v is not None else 0


class SResumeUserRead(BaseModel):
    id: int
    surname: str
    name: str
    last_name: str | None = None
    birthdate: date | None = None
    sex: bool | None = None
    location: SBaseCatalogItemRead | None = None
    edu_institution_id: int | None = None
    edu_level_id: int | None = None
    edu_status: EduStatus | None = None
    applicant: SApplicantRead | None = Field(..., exclude=True)

    def model_post_init(self, __context: Any):
        self.edu_institution_id = self.applicant.edu_institution_id
        self.edu_level_id = self.applicant.edu_level_id
        self.edu_status = self.applicant.edu_status


class SResumeRead(BaseModel):
    id: int
    position: str
    specialization: str
    salary: int | None
    description: str
    user: SResumeUserRead | None = Field(..., serialization_alias="applicant")
    resume_types: list[SBaseCatalogItemRead]
    resume_formats: list[SBaseCatalogItemRead]

    def model_post_init(self, __context: Any):
        if self.salary == 0:
            self.salary = None
