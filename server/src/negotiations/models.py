from typing import Optional
from datetime import datetime
from enum import Enum

import sqlalchemy as alch
import sqlalchemy.orm as orm

from sqlalchemy import DateTime
from sqlalchemy.sql import func

from src.database import Base
from src.users.models import User
from src.vacancies.models import Vacancy


class NegotiationStatus(Enum):
    PENDING = 'pending'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'


class Negotiation(Base):
    __tablename__ = 'negotiations'
    __table_args__ = (
        alch.UniqueConstraint('vacancy_id', 'applicant_id', name='uix_negotiation_vacancy_applicant'),
    )

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    status: orm.Mapped[str] = orm.mapped_column(alch.String(), default=NegotiationStatus.PENDING.value)
    employer_description: orm.Mapped[str] = orm.mapped_column(alch.String(150), nullable=True)
    applicant_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("users.id", ondelete='CASCADE'), index=True
    )
    employer_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("users.id", ondelete='CASCADE'), index=True
    )
    vacancy_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("vacancies.id", ondelete='CASCADE'), index=True
    )
    timestamp: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    applicant: orm.Mapped[Optional["User"]] = orm.relationship(
        uselist=False,
        passive_deletes=True,
        foreign_keys=(applicant_id,)
    )
    employer: orm.Mapped[Optional["User"]] = orm.relationship(
        uselist=False,
        passive_deletes=True,
        foreign_keys=(employer_id,)
    )
    vacancy: orm.Mapped[Optional["Vacancy"]] = orm.relationship(
        uselist=False,
        passive_deletes=True
    )
