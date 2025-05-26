from datetime import date

import sqlalchemy as alch
import sqlalchemy.orm as orm

from sqlalchemy import Date

from src.database import Base


class Company(Base):
    __tablename__ = 'companies'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(120), index=True, unique=True)
    registration_date: orm.Mapped[date] = orm.mapped_column(Date(), nullable=True)
    inn: orm.Mapped[str] = orm.mapped_column(alch.String(12), unique=True, nullable=True)
    address: orm.Mapped[str] = orm.mapped_column(alch.String(120), nullable=True)
    description: orm.Mapped[str] = orm.mapped_column(alch.String(5000), nullable=True)
    is_verified: orm.Mapped[bool] = orm.mapped_column(alch.Boolean(), default=False)
