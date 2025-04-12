from datetime import datetime

import sqlalchemy as alch
import sqlalchemy.orm as orm

from sqlalchemy import DateTime
from sqlalchemy.sql import func

from src.database import Base

vacancies_types = alch.Table(
    "vacancies_types",
    Base.metadata,
    alch.Column(
        "vacancy_id",
        alch.Integer, alch.ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True, index=True
    ),
    alch.Column(
        "type_id",
        alch.Integer,
        alch.ForeignKey("employment_types.id", ondelete="CASCADE"),
        primary_key=True, index=True
    )
)

vacancies_formats = alch.Table(
    "vacancies_formats",
    Base.metadata,
    alch.Column(
        "vacancy_id",
        alch.Integer, alch.ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True, index=True
    ),
    alch.Column(
        "format_id",
        alch.Integer,
        alch.ForeignKey("employment_formats.id", ondelete="CASCADE"),
        primary_key=True, index=True
    )
)

vacancies_schedules = alch.Table(
    "vacancies_schedules",
    Base.metadata,
    alch.Column(
        "vacancy_id",
        alch.Integer, alch.ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True, index=True
    ),
    alch.Column(
        "schedule_id",
        alch.Integer,
        alch.ForeignKey("employment_schedules.id", ondelete="CASCADE"),
        primary_key=True, index=True
    )
)


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    position: orm.Mapped[str] = orm.mapped_column(
        alch.String(120), nullable=False
    )
    specialization: orm.Mapped[str] = orm.mapped_column(
        alch.String(120), nullable=False
    )
    salary: orm.Mapped[int] = orm.mapped_column(alch.Integer(), server_default='0')
    description: orm.Mapped[str] = orm.mapped_column(alch.String(500))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    company_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("companies.id", ondelete='CASCADE'), index=True
    )

    vacancy_types: orm.Mapped[list["EmploymentType"]] = orm.relationship(
        "EmploymentType", secondary=vacancies_types
    )
    vacancy_formats: orm.Mapped[list["EmploymentFormat"]] = orm.relationship(
        "EmploymentFormat", secondary=vacancies_formats
    )
    vacancy_schedules: orm.Mapped[list["EmploymentSchedule"]] = orm.relationship(
        "EmploymentSchedule", secondary=vacancies_schedules
    )


class EmploymentType(Base):
    __tablename__ = 'employment_types'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(
        alch.String(20), nullable=False
    )


class EmploymentFormat(Base):
    __tablename__ = 'employment_formats'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(
        alch.String(20), nullable=False
    )


class EmploymentSchedule(Base):
    __tablename__ = 'employment_schedules'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(
        alch.String(20), nullable=False
    )
