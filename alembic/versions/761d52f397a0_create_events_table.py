"""create events table

Revision ID: 761d52f397a0
Revises: 
Create Date: 2025-07-31 00:07:41.406983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '761d52f397a0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('events', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('name', sa.String, nullable=False), 
                    sa.Column('description', sa.String, nullable=True), sa.Column('date', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')), 
                    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('events')
    """Downgrade schema."""
    pass
