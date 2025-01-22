from sqlalchemy import Column, String, Boolean, Enum, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
import enum
from uuid import uuid4

# Table d'association pour les rôles et permissions
role_permission = Table('role_permission', Base.metadata,
    Column('role_id', String, ForeignKey('roles.id')),
    Column('permission_id', String, ForeignKey('permissions.id'))
)

class TypeRole(str, enum.Enum):
    """Types de rôles système"""
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SUPERVISEUR = "SUPERVISEUR"
    OPERATEUR = "OPERATEUR"
    CONSULTANT = "CONSULTANT"

class Permission(Base):
    """Modèle pour les permissions système"""
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    module = Column(String(50))  # Module concerné
    actions = Column(JSON)  # Actions autorisées (create, read, update, delete)

class Role(Base):
    """Modèle pour les rôles utilisateur"""
    __tablename__ = "roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    type = Column(Enum(TypeRole), nullable=False)
    permissions = relationship("Permission", secondary=role_permission)
    is_active = Column(Boolean, default=True)

class Utilisateur(Base):
    """Modèle pour les utilisateurs du système"""
    __tablename__ = "utilisateurs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    nom = Column(String(100))
    prenom = Column(String(100))
    role_id = Column(String, ForeignKey('roles.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    preferences = Column(JSON)  # Préférences utilisateur (thème, langue, etc.)
    derniere_connexion = Column(String(100))

    # Relations
    role = relationship("Role")
    notifications = relationship("Notification", back_populates="utilisateur")