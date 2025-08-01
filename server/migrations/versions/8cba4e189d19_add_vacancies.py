"""add vacancies

Revision ID: 8cba4e189d19
Revises: 1a77bf5dba0e
Create Date: 2025-04-02 14:09:11.925902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cba4e189d19'
down_revision: Union[str, None] = '1a77bf5dba0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employment_formats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employment_schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employment_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.String(length=120), nullable=False),
    sa.Column('specialization', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vacancies_company_id'), 'vacancies', ['company_id'], unique=False)
    op.create_table('vacancies_formats',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('format_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['format_id'], ['employment_formats.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'format_id')
    )
    op.create_table('vacancies_schedules',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['employment_schedules.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'schedule_id')
    )
    op.create_table('vacancies_types',
    sa.Column('vacancy_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['employment_types.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vacancy_id', 'type_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancies_types')
    op.drop_table('vacancies_schedules')
    op.drop_table('vacancies_formats')
    op.drop_index(op.f('ix_vacancies_company_id'), table_name='vacancies')
    op.drop_table('vacancies')
    op.drop_table('employment_types')
    op.drop_table('employment_schedules')
    op.drop_table('employment_formats')
    # ### end Alembic commands ###
