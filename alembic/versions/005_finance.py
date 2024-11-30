"""Ajout des tables financières

Revision ID: 005
Revises: 004
Create Date: 2024-01-20 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

def upgrade():
    # Table des comptes
    op.create_table(
        'comptes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('numero', sa.String(50), nullable=False),
        sa.Column('libelle', sa.String(200), nullable=False),
        sa.Column('type_compte', sa.String(20), nullable=False),
        sa.Column('devise', sa.String(3), default='XAF'),
        sa.Column('solde', sa.Numeric(15, 2), default=0),
        sa.Column('banque', sa.String(100)),
        sa.Column('iban', sa.String(50)),
        sa.Column('swift', sa.String(20)),
        sa.Column('actif', sa.Boolean(), default=True),
        sa.Column('description', sa.Text),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero'),
        sa.CheckConstraint("type_compte IN ('BANQUE', 'CAISSE', 'EPARGNE')", name='check_type_compte')
    )

    # Table des transactions
    op.create_table(
        'transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reference', sa.String(50), nullable=False),
        sa.Column('date_transaction', sa.DateTime, nullable=False),
        sa.Column('type_transaction', sa.String(20), nullable=False),
        sa.Column('categorie', sa.String(20), nullable=False),
        sa.Column('montant', sa.Numeric(15, 2), nullable=False),
        sa.Column('devise', sa.String(3), default='XAF'),
        sa.Column('description', sa.Text),
        sa.Column('statut', sa.String(20), nullable=False),
        sa.Column('compte_source_id', postgresql.UUID(as_uuid=True)),
        sa.Column('compte_destination_id', postgresql.UUID(as_uuid=True)),
        sa.Column('piece_jointe', sa.String(500)),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('validee_par_id', postgresql.UUID(as_uuid=True)),
        sa.Column('date_validation', sa.DateTime),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['compte_source_id'], ['comptes.id']),
        sa.ForeignKeyConstraint(['compte_destination_id'], ['comptes.id']),
        sa.ForeignKeyConstraint(['validee_par_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('reference'),
        sa.CheckConstraint("type_transaction IN ('RECETTE', 'DEPENSE', 'VIREMENT')", name='check_type_transaction'),
        sa.CheckConstraint("categorie IN ('VENTE', 'ACHAT_INTRANT', 'SALAIRE', 'MAINTENANCE', 'TRANSPORT', 'AUTRE')", name='check_categorie_transaction'),
        sa.CheckConstraint("statut IN ('EN_ATTENTE', 'VALIDEE', 'REJETEE', 'ANNULEE')", name='check_statut_transaction')
    )

    # Table des budgets
    op.create_table(
        'budgets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('periode', sa.String(7), nullable=False),
        sa.Column('categorie', sa.String(20), nullable=False),
        sa.Column('montant_prevu', sa.Numeric(15, 2), nullable=False),
        sa.Column('montant_realise', sa.Numeric(15, 2), default=0),
        sa.Column('notes', sa.Text),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("categorie IN ('VENTE', 'ACHAT_INTRANT', 'SALAIRE', 'MAINTENANCE', 'TRANSPORT', 'AUTRE')", name='check_categorie_budget')
    )

def downgrade():
    op.drop_table('budgets')
    op.drop_table('transactions')
    op.drop_table('comptes')
