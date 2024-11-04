"""Ajout de la table notifications

Revision ID: 003
Revises: 002
Create Date: 2024-01-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # Création des enums
    op.execute("""
        CREATE TYPE typenotification AS ENUM (
            'INFO', 'SUCCESS', 'WARNING', 'ERROR'
        );
        CREATE TYPE modulenotification AS ENUM (
            'SYSTEME', 'PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE'
        );
    """)

    # Création de la table notifications
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('titre', sa.String(200), nullable=False),
        sa.Column('message', sa.String(500), nullable=False),
        sa.Column('type', sa.Enum('INFO', 'SUCCESS', 'WARNING', 'ERROR', name='typenotification'), nullable=False),
        sa.Column('module', sa.Enum('SYSTEME', 'PRODUCTION', 'INVENTAIRE', 'RH', 'FINANCE', name='modulenotification'), nullable=False),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('lu', sa.Boolean(), default=False),
        sa.Column('destinataire_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('lien', sa.String(200)),
        sa.Column('donnees', postgresql.JSON(astext_type=sa.Text())),
        sa.ForeignKeyConstraint(['destinataire_id'], ['utilisateurs.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Index pour les requêtes fréquentes
    op.create_index(
        'ix_notifications_destinataire_id_lu',
        'notifications',
        ['destinataire_id', 'lu']
    )
    op.create_index(
        'ix_notifications_date_creation',
        'notifications',
        ['date_creation']
    )

def downgrade():
    op.drop_index('ix_notifications_date_creation')
    op.drop_index('ix_notifications_destinataire_id_lu')
    op.drop_table('notifications')
    op.execute('DROP TYPE modulenotification')
    op.execute('DROP TYPE typenotification')