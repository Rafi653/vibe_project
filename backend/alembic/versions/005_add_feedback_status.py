"""Add feedback status field

Revision ID: 005
Revises: 004
Create Date: 2025-10-11 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005'
down_revision: Union[str, None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE feedbackstatus AS ENUM ('open', 'actively_looking', 'resolved', 'cannot_work_on')")
    # Add status column with default value 'open'
    op.add_column('feedback', 
        sa.Column('status', 
                  sa.Enum('open', 'actively_looking', 'resolved', 'cannot_work_on', name='feedbackstatus'),
                  nullable=False,
                  server_default='open'))


def downgrade() -> None:
    op.drop_column('feedback', 'status')
    # Drop the enum type (PostgreSQL specific)
    op.execute("DROP TYPE IF EXISTS feedbackstatus")
