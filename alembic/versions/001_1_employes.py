"""Ajout de la table employes

Revision ID: 001_1
Revises: 001
Create Date: 2024-01-20 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_1'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Création de la table des employés
    op.create_table(
        'employes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('matricule', sa.String(50), nullable=False),
        sa.Column('nom', sa.String(100), nullable=False),
        sa.Column('prenom', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('date_naissance', sa.Date),
        sa.Column('date_embauche', sa.Date, nullable=False),
        sa.Column('poste', sa.String(100), nullable=False),
        sa.Column('departement', sa.String(100)),
        sa.Column('superieur_id', postgresql.UUID(as_uuid=True)),
        sa.Column('utilisateur_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statut', sa.String(20), nullable=False),
        sa.Column('donnees_supplementaires', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('matricule'),
        sa.UniqueConstraint('email'),
        sa.CheckConstraint("statut IN ('ACTIF', 'INACTIF', 'CONGE', 'SUSPENDU')", name='check_employe_statut')
    )

    # Ajout de la contrainte de clé étrangère pour superieur_id après la création de la table
    op.create_foreign_key(
        'fk_employe_superieur',
        'employes',
        'employes',
        ['superieur_id'],
        ['id']
    )

def downgrade():
    op.drop_constraint('fk_employe_superieur', 'employes', type_='foreignkey')
    op.drop_table('employes')
