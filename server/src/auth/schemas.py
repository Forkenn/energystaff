from pydantic import BaseModel, EmailStr, model_validator
from fastapi_users import schemas

class SUserRead(schemas.BaseUser[int]):
    pass

class SUserCreate(schemas.CreateUpdateDictModel):
    surname: str
    name: str
    email: EmailStr
    password: str
    is_edu: bool = False
    is_employer: bool = False
    is_applicant: bool = False

    @model_validator(mode="after")
    def check_roles(self):
        if sum((self.is_edu, self.is_applicant, self.is_employer)) != 1:
            raise ValueError("User can only have one role")
        return self

class SUserCreateBase(BaseModel):
    surname: str
    name: str
    email: EmailStr
    password: str

class SEmployerCreate(SUserCreateBase):
    company_id: int | None = None
    company_name: str | None = None

    @model_validator(mode="after")
    def check_company(self):
        if (self.company_id is None) == (self.company_name is None):
            raise ValueError("Only id OR company name required")
        return self

class SEduCreate(SUserCreateBase):
    edu_institution_id: int

class SUserUpdate(schemas.BaseUserUpdate):
    pass
