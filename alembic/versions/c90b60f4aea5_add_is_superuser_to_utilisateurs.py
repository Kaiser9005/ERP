"""add_is_superuser_to_utilisateurs

Revision ID: c90b60f4aea5
Revises: e60f0483a82e
Create Date: 2025-01-21 03:09:11.065732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c90b60f4aea5'
down_revision: Union[str, None] = 'e60f0483a82e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('utilisateurs', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('utilisateurs', 'is_superuser')