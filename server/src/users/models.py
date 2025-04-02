from datetime import date

import sqlalchemy as alch
import sqlalchemy.orm as orm

from typing import Optional

from sqlalchemy import Date
from fastapi_users.db import SQLAlchemyBaseUserTable

from src.database import Base
#from src.tools.models import EduInstitution, EduLevel, Location
#TODO: abstract relationships


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True, unique=True)
    surname: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True)
    last_name: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True, nullable=True)
    birthdate: orm.Mapped[date] = orm.mapped_column(Date(), nullable=True)
    #sex: orm.Mapped[bool] = orm.mapped_column(alch.Boolean, nullable=True)
    is_edu: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)
    is_employer: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)
    is_applicant: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)

    applicant: orm.Mapped[Optional["Applicant"]] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    employer: orm.Mapped[Optional["Employer"]] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    edu_worker: orm.Mapped[Optional["EduWorker"]] = orm.relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # fastapi-users fields by default:
    # hashed_password: orm.Mapped[str] = orm.mapped_column(String(256))
    # is_verified: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)
    # is_active: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)
    # is_superuser: orm.Mapped[bool] = orm.mapped_column(Boolean(), default=False)


class Applicant(Base):
    __tablename__ = 'applicants'

    user_id: orm.Mapped[int] = orm.mapped_column(
        alch.Integer(), alch.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True
    )
    edu_institution_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("edu_institutions.id", ondelete='SET NULL'), nullable=True
    )
    edu_level_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("edu_levels.id", ondelete='SET NULL'), nullable=True
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="applicant")


class Employer(Base):
    __tablename__ = 'employers'

    user_id: orm.Mapped[int] = orm.mapped_column(
        alch.Integer(), alch.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True
    )
    company_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("companies.id", ondelete='CASCADE')
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="employer")


class EduWorker(Base):
    __tablename__ = 'edu_workers'

    user_id: orm.Mapped[int] = orm.mapped_column(
        alch.Integer(), alch.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True
    )
    edu_institution_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("edu_institutions.id", ondelete='CASCADE'), nullable=False
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="edu_worker")
