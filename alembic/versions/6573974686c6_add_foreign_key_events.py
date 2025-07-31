"""add_foreign_key_events

Revision ID: 6573974686c6
Revises: 7f8779a6ed87
Create Date: 2025-07-31 00:41:11.458518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6573974686c6'
down_revision: Union[str, Sequence[str], None] = '7f8779a6ed87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('events') as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.Integer, nullable=False))
        batch_op.create_foreign_key(
            'events_users_fk',
            referent_table='users',
            local_cols=['owner_id'],
            remote_cols=['id'],
            ondelete='CASCADE'
        )


def downgrade():
    with op.batch_alter_table('events') as batch_op:
        batch_op.drop_constraint('events_users_fk', type_='foreignkey')
        batch_op.drop_column('owner_id')