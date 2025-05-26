import sqlalchemy as alch
import sqlalchemy.orm as orm

from src.database import Base


class ProofDocument(Base):
    __tablename__='proof_documents'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    recommendation_id: orm.Mapped[int] = orm.mapped_column(
        alch.ForeignKey("recommendations.id", ondelete='CASCADE'), index=True
    )
    download_name: orm.Mapped[str] = orm.mapped_column(alch.String(256))
    real_name: orm.Mapped[str] = orm.mapped_column(alch.String(256))
    size: orm.Mapped[int] = orm.mapped_column(alch.Integer())


class Recommendation(Base):
    __tablename__='recommendations'

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    description: orm.Mapped[str] = orm.mapped_column(alch.String(5000))
    applicant_id = orm.mapped_column(
        alch.ForeignKey("users.id", ondelete='CASCADE'), index=True, unique=True
    )

    documents: orm.Mapped[list["ProofDocument"]] = orm.relationship(
        "ProofDocument", cascade='all, delete-orphan'
    )
