"""Create initial tables

Revision ID: cf232274005e
Revises: 
Create Date: 2026-05-25 20:49:47.945948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'cf232274005e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create regions table
    op.create_table(
        'regions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_regions_name'), 'regions', ['name'], unique=False)

    # Create courts table
    op.create_table(
        'courts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('address', sa.String(length=300), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('region_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courts_name'), 'courts', ['name'], unique=False)
    op.create_index(op.f('ix_courts_region_id'), 'courts', ['region_id'], unique=False)

    # Create availability_status enum
    op.execute("CREATE TYPE availability_status AS ENUM ('available', 'reserved', 'unavailable')")

    # Create availability table
    op.create_table(
        'availability',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('court_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('time_slot', sa.String(length=20), nullable=False),
        sa.Column('status', postgresql.ENUM('available', 'reserved', 'unavailable', name='availability_status'), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['court_id'], ['courts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('court_id', 'date', 'time_slot', name='uq_court_date_time')
    )
    op.create_index(op.f('ix_availability_court_id'), 'availability', ['court_id'], unique=False)
    op.create_index(op.f('ix_availability_date'), 'availability', ['date'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_availability_date'), table_name='availability')
    op.drop_index(op.f('ix_availability_court_id'), table_name='availability')
    op.drop_table('availability')
    op.execute("DROP TYPE availability_status")

    op.drop_index(op.f('ix_courts_region_id'), table_name='courts')
    op.drop_index(op.f('ix_courts_name'), table_name='courts')
    op.drop_table('courts')

    op.drop_index(op.f('ix_regions_name'), table_name='regions')
    op.drop_table('regions')
