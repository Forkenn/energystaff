from pydantic import EmailStr, model_validator
from fastapi_users import schemas

class SUserRead(schemas.BaseUser[int]):
    pass

class SUserCreate(schemas.CreateUpdateDictModel):
    surname: str
    name: str
    email: EmailStr
    password: str
    is_edu: bool
    is_employer: bool
    is_applicant: bool

    @model_validator(mode="after")
    def check_roles(self):
        if sum((self.is_edu, self.is_applicant, self.is_employer)) != 1:
            raise ValueError("User can only have one role")
        return self


class SUserUpdate(schemas.BaseUserUpdate):
    pass
