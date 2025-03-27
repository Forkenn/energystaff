import sqlalchemy as alch
import sqlalchemy.orm as orm

from src.database import Base

class EduInstitution(Base):
    __tablename__ = 'edu_institutions'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(240))

class EduLevel(Base):
    __tablename__ = 'edu_levels'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(15))

class Location(Base):
    __tablename__ = 'locations'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(alch.String(25))
