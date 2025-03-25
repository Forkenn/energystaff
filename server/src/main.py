from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.config import auth_backend
from .auth.manager import fastapi_users
from .auth.schemas import SUserRead, SUserCreate

app = FastAPI(title='EnergyStaff', root_path='/api')

origins = [
    "http://127.0.0.1",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), tags=["Auth"]
)

app.include_router(
    fastapi_users.get_register_router(SUserRead, SUserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)
