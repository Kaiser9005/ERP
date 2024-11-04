"""Ajout des tables de gestion de projet

Revision ID: 004
Revises: 003
Create Date: 2024-01-20 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade():
    # Création des enums
    op.execute("""
        CREATE TYPE projectstatus AS ENUM (
            'PLANIFIE', 'EN_COURS', 'EN_PAUSE', 'TERMINE', 'ANNULE'
        );
        CREATE TYPE taskpriority AS ENUM (
            'BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE'
        );
        CREATE TYPE taskstatus AS ENUM (
            'A_FAIRE', 'EN_COURS', 'EN_REVUE', 'TERMINE', 'BLOQUE'
        );
    """)

    # Table des projets
    op.create_table(
        'projets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('nom', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('date_debut', sa.Date, nullable=False),
        sa.Column('date_fin_prevue', sa.Date, nullable=False),
        sa.Column('date_fin_reelle', sa.Date),
        sa.Column('statut', sa.Enum('PLANIFIE', 'EN_COURS', 'EN_PAUSE', 'TERMINE', 'ANNULE', name='projectstatus'), nullable=False),
        sa.Column('budget', sa.Numeric(10, 2)),
        sa.Column('responsable_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('objectifs', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('risques', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['responsable_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Table des tâches
    op.create_table(
        'taches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('projet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('titre', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('priorite', sa.Enum('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE', name='taskpriority'), nullable=False),
        sa.Column('statut', sa.Enum('A_FAIRE', 'EN_COURS', 'EN_REVUE', 'TERMINE', 'BLOQUE', name='taskstatus'), nullable=False),
        sa.Column('date_debut', sa.DateTime),
        sa.Column('date_fin_prevue', sa.DateTime, nullable=False),
        sa.Column('date_fin_reelle', sa.DateTime),
        sa.Column('assignee_id', postgresql.UUID(as_uuid=True)),
        sa.Column('temps_estime', sa.Numeric(5, 2)),
        sa.Column('temps_passe', sa.Numeric(5, 2)),
        sa.Column('dependances', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['projet_id'], ['projets.id']),
        sa.ForeignKeyConstraint(['assignee_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Table des commentaires
    op.create_table(
        'commentaires_tache',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tache_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('auteur_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contenu', sa.Text, nullable=False),
        sa.Column('date_creation', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['tache_id'], ['taches.id']),
        sa.ForeignKeyConstraint(['auteur_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Table des documents
    op.create_table(
        'documents_projet',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('projet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nom', sa.String(200), nullable=False),
        sa.Column('type', sa.String(50)),
        sa.Column('chemin_fichier', sa.String(500), nullable=False),
        sa.Column('date_upload', sa.DateTime, nullable=False),
        sa.Column('uploaded_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['projet_id'], ['projets.id']),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('documents_projet')
    op.drop_table('commentaires_tache')
    op.drop_table('taches')
    op.drop_table('projets')
    op.execute('DROP TYPE taskstatus')
    op.execute('DROP TYPE taskpriority')
    op.execute('DROP TYPE projectstatus')