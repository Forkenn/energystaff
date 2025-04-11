from datetime import date

from pydantic import BaseModel, Field


class SApplicantRead(BaseModel):
    edu_institution_id: int | None = None
    edu_level_id: int | None = None


class SEmployerRead(BaseModel):
    company_id: int


class SEduWorkerRead(BaseModel):
    edu_institution_id: int


class SUserReadFull(BaseModel):
    id: int
    email: str
    surname: str
    name: str
    last_name: str | None = None
    birthdate: date | None = None
    #sex: str
    is_edu: bool
    is_employer: bool
    is_applicant: bool
    is_verified: bool
    is_active: bool
    is_superuser: bool
    applicant: SApplicantRead | None = None
    employer: SEmployerRead | None = None
    edu_worker: SEduWorkerRead | None = None


class SUserEdit(BaseModel):
    surname: str = Field(
        default=...,
        min_length=2,
        max_length=120,
        description="User surname from 2 to 120 symbols"
    )
    name: str  = Field(
        default=...,
        min_length=3,
        max_length=120,
        description="User name from 3 to 120 symbols"
    )
    last_name: str | None = Field(
        default=...,
        min_length=0,
        max_length=120,
        description="User last name from 0 to 120 symbols"
    )
    birthdate: date | None = None
    #sex: str
