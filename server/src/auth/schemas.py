from pydantic import EmailStr
from fastapi_users import schemas

class SUserRead(schemas.BaseUser[int]):
    pass

class SUserCreate(schemas.CreateUpdateDictModel):
    surname: str
    name: str
    email: EmailStr
    password: str

class SUserUpdate(schemas.BaseUserUpdate):
    pass
