import sqlalchemy as alch

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.repositories.common import CommonRepository
from src.recommendations.models import Recommendation, ProofDocument

from src.users.models import Applicant


class RecommendationRepository(CommonRepository[Recommendation]):
    def __init__(self, session: AsyncSession):
        super().__init__(Recommendation, session)

    async def get_by_uid(self, uid: int) -> Recommendation | None:
        query = (
            alch.select(Recommendation)
            .where(Recommendation.applicant_id == uid)
        )

        return (await self.session.execute(query)).scalar()
    
    async def get_full(self, id: int) -> Recommendation | None:
        query = (
            alch.select(Recommendation)
            .where(Recommendation.id == id)
            .options(joinedload(Recommendation.documents))
        )

        return (await self.session.execute(query)).scalar()
    
    async def get_full_secured(self,
            id: int, edu_institution_id: int
    ) -> Recommendation | None:
        query = (
            alch.select(Recommendation)
            .join(Applicant, Applicant.user_id == Recommendation.applicant_id)
            .where(
                Recommendation.id == id,
                Applicant.edu_institution_id == edu_institution_id
            )
            .options(joinedload(Recommendation.documents))
        )

        return (await self.session.execute(query)).scalar()

    async def get_full_by_uid(self, uid: int) -> Recommendation | None:
        query = (
            alch.select(Recommendation)
            .where(Recommendation.applicant_id == uid)
            .options(joinedload(Recommendation.documents))
        )

        return (await self.session.execute(query)).scalar()
    
    async def get_full_by_uid_secured_edu(
            self, uid: int, edu_institution_id: int
    ) -> Recommendation | None:
        query = (
            alch.select(Recommendation)
            .join(Applicant, Applicant.user_id == Recommendation.applicant_id)
            .where(
                Recommendation.applicant_id == uid,
                Applicant.edu_institution_id == edu_institution_id
            )
            .options(joinedload(Recommendation.documents))
        )

        return (await self.session.execute(query)).scalar()
    
    async def create(
            self,
            documents: list[ProofDocument],
            data: dict
    ) -> Recommendation:
        recommendation: Recommendation = self.model(**data)
        recommendation.documents = documents

        self.session.add(recommendation)
        await self.session.commit()
        return recommendation

    async def update(
            self,
            recommendation: Recommendation,
            data: dict
    ) -> None:
        for field, value in data.items():
            setattr(recommendation, field, value)

        await self.session.commit()

    async def exists_by_uid(self, uid: int) -> bool:
        query = alch.select(1).where(Recommendation.applicant_id == uid)
        result = await self.session.scalar(query)
        return result is not None
