"""Add profile fields for clients and coaches

Revision ID: 003
Revises: 002
Create Date: 2025-10-11 10:21:05.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add client-specific profile fields
    op.add_column('users', sa.Column('height', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('weight', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('bicep_size', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('waist', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('target_goals', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('dietary_restrictions', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('health_complications', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('injuries', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('gym_access', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('supplements', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('referral_source', sa.String(length=255), nullable=True))
    
    # Add coach-specific profile fields
    op.add_column('users', sa.Column('track_record', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('experience', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('certifications', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('competitions', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('qualifications', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('specialties', sa.Text(), nullable=True))
    
    # Add custom fields JSON column for extensibility
    op.add_column('users', sa.Column('custom_fields', sa.JSON(), nullable=True))


def downgrade() -> None:
    # Remove all added columns
    op.drop_column('users', 'custom_fields')
    op.drop_column('users', 'specialties')
    op.drop_column('users', 'qualifications')
    op.drop_column('users', 'competitions')
    op.drop_column('users', 'certifications')
    op.drop_column('users', 'experience')
    op.drop_column('users', 'track_record')
    op.drop_column('users', 'referral_source')
    op.drop_column('users', 'supplements')
    op.drop_column('users', 'gym_access')
    op.drop_column('users', 'injuries')
    op.drop_column('users', 'health_complications')
    op.drop_column('users', 'dietary_restrictions')
    op.drop_column('users', 'target_goals')
    op.drop_column('users', 'waist')
    op.drop_column('users', 'bicep_size')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'age')
    op.drop_column('users', 'weight')
    op.drop_column('users', 'height')
