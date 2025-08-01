"""add negotiation description

Revision ID: fd76eb581b85
Revises: 7be62b307542
Create Date: 2025-04-14 13:25:52.900553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd76eb581b85'
down_revision: Union[str, None] = '7be62b307542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('negotiations', sa.Column('employer_description', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('negotiations', 'employer_description')
    # ### end Alembic commands ###
