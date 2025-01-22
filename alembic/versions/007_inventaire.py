"""Ajout des tables d'inventaire

Revision ID: 007
Revises: 006
Create Date: 2025-01-21 00:28:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '007'
down_revision: Union[str, None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Table des produits
    op.create_table(
        'produits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('nom', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('categorie', sa.String(20), nullable=False),
        sa.Column('unite_mesure', sa.String(20), nullable=False),
        sa.Column('prix_unitaire', sa.Float()),
        sa.Column('seuil_alerte', sa.Float()),
        sa.Column('specifications', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('conditions_stockage', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('date_derniere_maj', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.CheckConstraint("categorie IN ('INTRANT', 'EQUIPEMENT', 'RECOLTE', 'EMBALLAGE', 'PIECE_RECHANGE')", name='check_categorie'),
        sa.CheckConstraint("unite_mesure IN ('KG', 'LITRE', 'UNITE', 'TONNE', 'METRE')", name='check_unite_mesure')
    )

    # Table des entrepôts
    op.create_table(
        'entrepots',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nom', sa.String(), nullable=False),
        sa.Column('adresse', sa.String()),
        sa.Column('capacite', sa.Float()),
        sa.Column('responsable_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('specifications', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('date_derniere_maj', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['responsable_id'], ['employes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Table des stocks
    op.create_table(
        'stocks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('produit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entrepot_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quantite', sa.Float(), nullable=False),
        sa.Column('valeur_unitaire', sa.Float()),
        sa.Column('emplacement', sa.String()),
        sa.Column('lot', sa.String()),
        sa.Column('date_peremption', sa.DateTime()),
        sa.Column('origine', sa.String()),
        sa.Column('certifications', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('conditions_actuelles', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('capteurs_id', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('date_derniere_maj', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['entrepot_id'], ['entrepots.id'], ),
        sa.ForeignKeyConstraint(['produit_id'], ['produits.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Table des mouvements de stock
    op.create_table(
        'mouvements_stock',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('produit_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type_mouvement', sa.String(20), nullable=False),
        sa.Column('quantite', sa.Float(), nullable=False),
        sa.Column('date_mouvement', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('entrepot_source_id', postgresql.UUID(as_uuid=True)),
        sa.Column('entrepot_destination_id', postgresql.UUID(as_uuid=True)),
        sa.Column('responsable_id', postgresql.UUID(as_uuid=True)),
        sa.Column('reference_document', sa.String()),
        sa.Column('notes', sa.String()),
        sa.Column('cout_unitaire', sa.Float()),
        sa.Column('conditions_transport', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('controle_qualite', postgresql.JSON(astext_type=sa.Text())),
        sa.ForeignKeyConstraint(['entrepot_destination_id'], ['entrepots.id'], ),
        sa.ForeignKeyConstraint(['entrepot_source_id'], ['entrepots.id'], ),
        sa.ForeignKeyConstraint(['produit_id'], ['produits.id'], ),
        sa.ForeignKeyConstraint(['responsable_id'], ['utilisateurs.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("type_mouvement IN ('ENTREE', 'SORTIE', 'TRANSFERT')", name='check_type_mouvement')
    )


def downgrade() -> None:
    op.drop_table('mouvements_stock')
    op.drop_table('stocks')
    op.drop_table('entrepots')
    op.drop_table('produits')