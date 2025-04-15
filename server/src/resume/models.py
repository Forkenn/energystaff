import sqlalchemy as alch
import sqlalchemy.orm as orm

from src.database import Base
from src.vacancies.models import EmploymentFormat, EmploymentType

resume_types = alch.Table(
    "resume_types",
    Base.metadata,
    alch.Column(
        "resume_id",
        alch.Integer, alch.ForeignKey("resume.id", ondelete="CASCADE"),
        primary_key=True, index=True
    ),
    alch.Column(
        "type_id",
        alch.Integer,
        alch.ForeignKey("employment_types.id", ondelete="CASCADE"),
        primary_key=True, index=True
    )
)

resume_formats = alch.Table(
    "resume_formats",
    Base.metadata,
    alch.Column(
        "resume_id",
        alch.Integer, alch.ForeignKey("resume.id", ondelete="CASCADE"),
        primary_key=True, index=True
    ),
    alch.Column(
        "format_id",
        alch.Integer,
        alch.ForeignKey("employment_formats.id", ondelete="CASCADE"),
        primary_key=True, index=True
    )
)


class Resume(Base):
    __tablename__='resume'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    position: orm.Mapped[str] = orm.mapped_column(
        alch.String(120), nullable=False
    )
    specialization: orm.Mapped[str] = orm.mapped_column(
        alch.String(120), nullable=True
    )
    salary: orm.Mapped[int] = orm.mapped_column(alch.Integer(), server_default='0')
    description: orm.Mapped[str] = orm.mapped_column(alch.String(500))
    user_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("users.id", ondelete='CASCADE'), index=True, unique=True
    )

    resume_types: orm.Mapped[list["EmploymentType"]] = orm.relationship(
        "EmploymentType", secondary=resume_types
    )
    resume_formats: orm.Mapped[list["EmploymentFormat"]] = orm.relationship(
        "EmploymentFormat", secondary=resume_formats
    )

