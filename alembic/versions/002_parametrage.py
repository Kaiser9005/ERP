"""Ajout des tables de paramétrage

Revision ID: 002
Revises: 001_1
Create Date: 2024-01-20 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001_1'
branch_labels = None
depends_on = None

def upgrade():
    # Création de la table des paramètres
    op.create_table(
        'parametres',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('libelle', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('type_parametre', sa.String(20), nullable=False),
        sa.Column('module', sa.String(20)),
        sa.Column('valeur', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('modifiable', sa.Boolean(), default=True),
        sa.Column('visible', sa.Boolean(), default=True),
        sa.Column('ordre', sa.Integer(), default=0),
        sa.Column('categorie', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.CheckConstraint("type_parametre IN ('GENERAL', 'MODULE', 'UTILISATEUR')", name='check_type_parametre'),
        sa.CheckConstraint("module IN ('PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', 'COMPTABILITE', 'PARAMETRAGE')", name='check_module')
    )

    # Création de la table des configurations des modules
    op.create_table(
        'configurations_modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('module', sa.String(20), nullable=False),
        sa.Column('actif', sa.Boolean(), default=True),
        sa.Column('configuration', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('ordre_affichage', sa.Integer(), default=0),
        sa.Column('icone', sa.String(50)),
        sa.Column('couleur', sa.String(20)),
        sa.Column('roles_autorises', postgresql.JSON(astext_type=sa.Text())),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('module'),
        sa.CheckConstraint("module IN ('PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', 'COMPTABILITE', 'PARAMETRAGE')", name='check_module')
    )

def downgrade():
    op.drop_table('configurations_modules')
    op.drop_table('parametres')
