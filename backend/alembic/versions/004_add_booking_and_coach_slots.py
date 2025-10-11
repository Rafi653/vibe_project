"""Add booking table and coach availability fields

Revision ID: 004
Revises: 003
Create Date: 2025-10-11 10:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new coach fields to users table
    op.add_column('users', sa.Column('strengths', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('available_slots', sa.Integer(), nullable=False, server_default='10'))
    
    # Create bookings table
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coach_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.Column('slot_number', sa.Integer(), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('pending', 'confirmed', 'completed', 'cancelled', name='bookingstatus'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['coach_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_id'), 'bookings', ['id'], unique=False)
    op.create_index(op.f('ix_bookings_coach_id'), 'bookings', ['coach_id'], unique=False)
    op.create_index(op.f('ix_bookings_client_id'), 'bookings', ['client_id'], unique=False)


def downgrade() -> None:
    # Drop bookings table
    op.drop_index(op.f('ix_bookings_client_id'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_coach_id'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_id'), table_name='bookings')
    op.drop_table('bookings')
    
    # Drop enum type
    op.execute('DROP TYPE bookingstatus')
    
    # Remove coach fields from users table
    op.drop_column('users', 'available_slots')
    op.drop_column('users', 'strengths')
