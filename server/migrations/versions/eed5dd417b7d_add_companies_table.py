"""add companies table

Revision ID: eed5dd417b7d
Revises: f8defb651643
Create Date: 2025-03-27 14:01:15.573876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eed5dd417b7d'
down_revision: Union[str, None] = 'f8defb651643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('registration_date', sa.Date(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
