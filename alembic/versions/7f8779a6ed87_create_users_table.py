"""create_users_table

Revision ID: 7f8779a6ed87
Revises: a14f3e7c87dc
Create Date: 2025-07-31 00:27:01.859663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f8779a6ed87'
down_revision: Union[str, Sequence[str], None] = 'a14f3e7c87dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True, nullable=False), 
                    sa.Column('username', sa.String, nullable=False, unique=True),
                    sa.Column('email', sa.String, nullable=False, unique=True), 
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
