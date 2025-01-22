"""add_is_staff_to_utilisateurs

Revision ID: fc2b785e4229
Revises: c90b60f4aea5
Create Date: 2025-01-21 03:11:33.065732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc2b785e4229'
down_revision: Union[str, None] = 'c90b60f4aea5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('utilisateurs', sa.Column('is_staff', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('utilisateurs', 'is_staff')