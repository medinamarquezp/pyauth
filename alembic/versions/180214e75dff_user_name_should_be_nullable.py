"""User name should be nullable

Revision ID: 180214e75dff
Revises: 59359c9bc9ed
Create Date: 2024-08-12 00:34:55.711078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '180214e75dff'
down_revision: Union[str, None] = '59359c9bc9ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('name',
                              existing_type=sa.VARCHAR(length=100),
                              nullable=True)


def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('name',
                              existing_type=sa.VARCHAR(length=100),
                              nullable=False)
