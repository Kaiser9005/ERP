"""Ajout de la table documents

Revision ID: 006
Revises: 005
Create Date: 2024-01-20 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None

def upgrade():
    # Création de l'enum
    op.execute("""
        CREATE TYPE typedocument AS ENUM (
            'CONTRAT', 'FACTURE', 'BON_LIVRAISON', 'PIECE_JOINTE', 'RAPPORT', 'AUTRE'
        );
    """)

    # Création de la table documents
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nom', sa.String(200), nullable=False),
        sa.Column('type_document', sa.Enum('CONTRAT', 'FACTURE', 'BON_LIVRAISON', 'PIECE_JOINTE', 'RAPPORT', 'AUTRE', name='typedocument'), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('chemin_fichier', sa.String(500), nullable=False),
        sa.Column('taille', sa.Integer),
        sa.Column('type_mime', sa.String(100)),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('module', sa.String(50)),
        sa.Column('reference_id', postgresql.UUID(as_uuid=True)),
        sa.Column('uploaded_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['employes.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Index pour les recherches fréquentes
    op.create_index(
        'ix_documents_module_reference',
        'documents',
        ['module', 'reference_id']
    )

def downgrade():
    op.drop_index('ix_documents_module_reference')
    op.drop_table('documents')
    op.execute('DROP TYPE typedocument')