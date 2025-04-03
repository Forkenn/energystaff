from datetime import date

from pydantic import BaseModel


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
