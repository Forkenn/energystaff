from datetime import date

import sqlalchemy as alch
import sqlalchemy.orm as orm

from sqlalchemy import Date
from fastapi_users.db import SQLAlchemyBaseUserTable

from src.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True, unique=True)
    surname: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True, nullable=True)
    birthdate: orm.Mapped[date] = orm.mapped_column(Date(), nullable=True)
    is_edu: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)
    is_employer: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)
    is_applicant: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)

    # fastapi-users fields by default:
    # hashed_password: orm.Mapped[str] = orm.mapped_column(String(256))
    # is_verified: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)
    # is_active: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)
    # is_superuser: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)
