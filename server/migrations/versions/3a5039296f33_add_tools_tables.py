"""add tools tables

Revision ID: 3a5039296f33
Revises: eed5dd417b7d
Create Date: 2025-03-27 14:28:04.425542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a5039296f33'
down_revision: Union[str, None] = 'eed5dd417b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('edu_institutions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edu_levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations')
    op.drop_table('edu_levels')
    op.drop_table('edu_institutions')
    # ### end Alembic commands ###
