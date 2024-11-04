"""Initial auth tables

Revision ID: 001
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Création de la table des permissions
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200)),
        sa.Column('module', sa.String(50)),
        sa.Column('actions', postgresql.JSON(astext_type=sa.Text())),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    # Création de la table des rôles
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nom', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200)),
        sa.Column('type', sa.Enum('ADMIN', 'MANAGER', 'SUPERVISEUR', 'OPERATEUR', 'CONSULTANT', name='typerole')),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nom')
    )

    # Création de la table d'association role_permission
    op.create_table(
        'role_permission',
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    # Création de la table des utilisateurs
    op.create_table(
        'utilisateurs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(200), nullable=False),
        sa.Column('nom', sa.String(100)),
        sa.Column('prenom', sa.String(100)),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('preferences', postgresql.JSON(astext_type=sa.Text())),
        sa.Column('derniere_connexion', sa.String(100)),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    op.drop_table('utilisateurs')
    op.drop_table('role_permission')
    op.drop_table('roles')
    op.drop_table('permissions')
    op.execute('DROP TYPE typerole')