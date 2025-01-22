"""Standardisation des noms dans les modèles

Revision ID: standardisation_noms_modeles
Revises: fc2b785e4229
Create Date: 2025-01-21 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'standardisation_noms_modeles'
down_revision = 'fc2b785e4229'
branch_labels = None
depends_on = None

def upgrade():
    # Renommer la contrainte de clé étrangère dans la table taches
    op.drop_constraint('taches_assignee_id_fkey', 'taches')
    op.create_foreign_key(
        'taches_responsable_id_fkey',
        'taches', 'employes',
        ['responsable_id'], ['id']
    )

def downgrade():
    # Restaurer la contrainte de clé étrangère dans la table taches
    op.drop_constraint('taches_responsable_id_fkey', 'taches')
    op.create_foreign_key(
        'taches_assignee_id_fkey',
        'taches', 'employes',
        ['responsable_id'], ['id']
    )