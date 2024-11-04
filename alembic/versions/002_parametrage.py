"""Ajout des tables de paramétrage

Revision ID: 002
Revises: 001
Create Date: 2024-01-20 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Création des enums
    op.execute("""
        CREATE TYPE typeparametre AS ENUM ('GENERAL', 'MODULE', 'UTILISATEUR');
        CREATE TYPE modulesysteme AS ENUM (
            'PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', 'COMPTABILITE', 'PARAMETRAGE'
        );
    """)

    # Création de la table des paramètres
    op.create_table(
        'parametres',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('libelle', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('type_parametre', sa.Enum('GENERAL', 'MODULE', 'UTILISATEUR', name='typeparametre'), nullable=False),
        sa.Column('module', sa.Enum('PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', 'COMPTABILITE', 'PARAMETRAGE', name='modulesysteme')),
        sa.Column('valeur', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('modifiable', sa.Boolean(), default=True),
        sa.Column('visible', sa.Boolean(), default=True),
        sa.Column('ordre', sa.Integer(), default=0),
        sa.Column('categorie', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Création de la table des configurations des modules
    op.create_table(
        'configurations_modules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('module', sa.Enum('PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', 'COMPTABILITE', 'PARAMETRAGE', name='modulesysteme'), nullable=False),
        sa.Column('actif', sa.Boolean(), default=True),
        sa.Column('configuration', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('ordre_affichage', sa.Integer(), default=0),
        sa.Column('icone', sa.String(50)),
        sa.Column('couleur', sa.String(20)),
        sa.Column('roles_autorises', postgresql.JSON(astext_type=sa.Text())),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('module')
    )

def downgrade():
    op.drop_table('configurations_modules')
    op.drop_table('parametres')
    op.execute('DROP TYPE modulesysteme')
    op.execute('DROP TYPE typeparametre')