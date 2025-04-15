from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.config import auth_backend
from .auth.manager import fastapi_users

from .auth.router import router as router_auth
from .users.router import router as router_users
from .tools.router import router as router_tools
from .vacancies.router import router as router_vacancies
from .companies.router import router as router_companies
from .negotiations.router import router as router_negotiations
from .resume.router import router as router_resume
from .recommendations.router import router as router_recommendations

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
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_resume)
app.include_router(router_recommendations)
app.include_router(router_companies)
app.include_router(router_vacancies)
app.include_router(router_negotiations)
app.include_router(router_tools)
