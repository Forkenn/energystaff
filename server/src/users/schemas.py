from datetime import date

from pydantic import BaseModel, Field

from src.core.schemas.common import SBaseQueryCountResponse, SBaseQuerySliceBody
from src.core.schemas.catalog import SBaseCatalogItemRead
from src.tools.models import EduStatus


class SUsersFilteredQuery(BaseModel):
    q: str | None = None
    birthdate: date | None = None
    location_id: int | None = None
    only_verified: bool | None = False


class SUsersReadQuery(SUsersFilteredQuery, SBaseQuerySliceBody):
    desc: bool | None = True


class SApplicantsFilteredQuery(BaseModel):
    q: str | None = None
    birthdate: date | None = None
    only_verified: bool | None = False
    location_id: int | None = None


class SApplicantsReadQuery(SApplicantsFilteredQuery, SBaseQuerySliceBody):
    pass


class SApplicantRead(BaseModel):
    edu_institution_id: int | None = None
    edu_level_id: int | None = None
    edu_status: EduStatus | None = None
    edu_number: str | None = None


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
    sex: bool | None = None
    is_edu: bool
    is_employer: bool
    is_applicant: bool
    is_verified: bool
    is_active: bool
    is_superuser: bool
    location: SBaseCatalogItemRead | None = None
    applicant: SApplicantRead | None = None
    employer: SEmployerRead | None = None
    edu_worker: SEduWorkerRead | None = None


class SUserPreview(BaseModel):
    id: int
    surname: str
    name: str
    last_name: str | None = None
    birthdate: date | None = None
    sex: bool | None = None
    is_edu: bool
    is_employer: bool
    is_applicant: bool
    is_verified: bool
    is_active: bool
    is_superuser: bool
    location: SBaseCatalogItemRead | None = None
    applicant: SApplicantRead | None = None
    employer: SEmployerRead | None = None
    edu_worker: SEduWorkerRead | None = None


class SUsersPreview(SBaseQueryCountResponse):
    items: list[SUserPreview]


class SApplicantPreview(BaseModel):
    id: int
    surname: str
    name: str
    last_name: str | None = None
    sex: bool | None = None
    birthdate: date | None = None
    is_verified: bool
    location: SBaseCatalogItemRead | None = None
    applicant: SApplicantRead | None = None


class SApplicantsPreview(SBaseQueryCountResponse):
    items: list[SApplicantPreview]


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
    sex: bool | None = None
    location_id: int | None = None
    applicant: SApplicantRead | None = None
