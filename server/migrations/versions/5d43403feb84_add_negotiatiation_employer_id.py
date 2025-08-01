"""add negotiatiation employer_id

Revision ID: 5d43403feb84
Revises: fd76eb581b85
Create Date: 2025-04-14 14:03:27.099167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d43403feb84'
down_revision: Union[str, None] = 'fd76eb581b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('negotiations', sa.Column('employer_id', sa.Integer(), nullable=True))

    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE negotiations n
        SET employer_id = (
            SELECT v.author_id
            FROM vacancies v
            WHERE v.id = n.vacancy_id
        )
    """))

    op.alter_column('negotiations', 'employer_id', nullable=False)
    op.create_index(op.f('ix_negotiations_employer_id'), 'negotiations', ['employer_id'], unique=False)
    op.create_foreign_key(None, 'negotiations', 'users', ['employer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'negotiations', type_='foreignkey')
    op.drop_index(op.f('ix_negotiations_employer_id'), table_name='negotiations')
    op.drop_column('negotiations', 'employer_id')
    # ### end Alembic commands ###
