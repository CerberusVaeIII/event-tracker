"""add_duration_events

Revision ID: a14f3e7c87dc
Revises: 761d52f397a0
Create Date: 2025-07-31 00:19:32.972987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a14f3e7c87dc'
down_revision: Union[str, Sequence[str], None] = '761d52f397a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('events', sa.Column('duration', sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('events', 'duration')
    pass
