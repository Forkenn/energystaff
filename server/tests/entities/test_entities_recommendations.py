import pytest
from src.users.models import User, Applicant
from src.companies.models import Company
from src.recommendations.models import Recommendation, ProofDocument

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_recommendation_with_documents(db_session: AsyncSession):
    user = User(email="rec@example.com", name="Rec", surname="Test", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    db_session.add(user)
    await db_session.commit()

    rec = Recommendation(applicant_id=user.id, description="Hard worker")
    doc = ProofDocument(recommendation_id=1, download_name="doc.pdf", real_name="original.pdf", size=2048)

    rec.documents=[doc]
    db_session.add(rec)
    await db_session.commit()
    await db_session.refresh(doc)
    await db_session.refresh(rec, attribute_names=('documents',))

    assert doc.download_name == "doc.pdf"
    assert rec.documents[0].download_name == "doc.pdf"


@pytest.mark.asyncio
async def test_recommendation_document_deletion(db_session: AsyncSession):
    user = User(email="rec@example.com", name="Rec", surname="Test", hashed_password="pwd", is_applicant=True)
    applicant = Applicant(user=user)
    db_session.add(user)
    await db_session.commit()

    rec = Recommendation(applicant_id=user.id, description="Hard worker")
    doc_1 = ProofDocument(recommendation_id=1, download_name="doc.pdf", real_name="original.pdf", size=2048)
    doc_2 = ProofDocument(recommendation_id=1, download_name="doc2.pdf", real_name="original2.pdf", size=2048)

    rec.documents=[doc_1, doc_2]
    db_session.add(rec)
    await db_session.commit()
    await db_session.refresh(doc_1)
    await db_session.refresh(rec, attribute_names=('documents',))

    assert rec.documents[0].download_name == "doc.pdf"
    assert rec.documents[1].download_name == "doc2.pdf"

    await db_session.delete(doc_1)
    await db_session.commit()
    await db_session.refresh(rec, attribute_names=('documents',))

    assert rec.documents[0].download_name == "doc2.pdf"
