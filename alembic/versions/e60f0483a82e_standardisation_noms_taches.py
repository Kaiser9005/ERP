"""standardisation_noms_taches

Revision ID: e60f0483a82e
Revises: 007
Create Date: 2025-01-21 00:18:32.616253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e60f0483a82e'
down_revision: Union[str, None] = '007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Création de la table ressource_tache
    op.create_table(
        'ressource_tache',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tache_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('produit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quantite_requise', sa.Float(), nullable=False),
        sa.Column('quantite_utilisee', sa.Float(), nullable=False),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('date_modification', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['produit_id'], ['produits.id'], ),
        sa.ForeignKeyConstraint(['tache_id'], ['taches.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Création de la table dependance_tache
    op.create_table(
        'dependance_tache',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tache_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dependance_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type_dependance', sa.String(length=50), nullable=False),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('date_modification', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['dependance_id'], ['taches.id'], ),
        sa.ForeignKeyConstraint(['tache_id'], ['taches.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Renommage des colonnes dans la table taches
    with op.batch_alter_table('taches') as batch_op:
        batch_op.alter_column('assignee_id', new_column_name='responsable_id')
        batch_op.alter_column('temps_estime', new_column_name='heures_estimees')
        batch_op.alter_column('temps_passe', new_column_name='heures_reelles')
        batch_op.add_column(sa.Column('dependant_meteo', sa.Boolean(), nullable=False, server_default='false'))
        batch_op.add_column(sa.Column('min_temperature', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('max_temperature', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('max_wind_speed', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('max_precipitation', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pourcentage_completion', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Suppression des colonnes ajoutées dans la table taches
    with op.batch_alter_table('taches') as batch_op:
        batch_op.drop_column('pourcentage_completion')
        batch_op.drop_column('max_precipitation')
        batch_op.drop_column('max_wind_speed')
        batch_op.drop_column('max_temperature')
        batch_op.drop_column('min_temperature')
        batch_op.drop_column('dependant_meteo')
        batch_op.alter_column('heures_reelles', new_column_name='temps_passe')
        batch_op.alter_column('heures_estimees', new_column_name='temps_estime')
        batch_op.alter_column('responsable_id', new_column_name='assignee_id')

    # Suppression des tables
    op.drop_table('dependance_tache')
    op.drop_table('ressource_tache')