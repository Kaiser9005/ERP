from sqlalchemy import Column, String, Boolean, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import enum
import uuid

class TypeModule(str, enum.Enum):
    """Types de modules système"""
    CORE = "CORE"
    FINANCE = "FINANCE"
    RH = "RH"
    PRODUCTION = "PRODUCTION"
    INVENTAIRE = "INVENTAIRE"
    ANALYTIQUE = "ANALYTIQUE"

class ModuleSysteme(Base):
    """Modèle représentant un module système"""
    __tablename__ = "modules_systeme"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    description = Column(String(500))
    type_module = Column(Enum(TypeModule), nullable=False)
    version = Column(String(20))
    actif = Column(Boolean, default=True)
    configuration = Column(JSON)  # Configuration spécifique au module
    dependances = Column(JSON)  # Liste des modules requis

    # Relations
    parametres = relationship("ParametreSysteme", back_populates="module")

class TypeParametre(str, enum.Enum):
    """Types de paramètres système"""
    GENERAL = "GENERAL"
    SECURITE = "SECURITE"
    NOTIFICATION = "NOTIFICATION"
    INTEGRATION = "INTEGRATION"
    PERFORMANCE = "PERFORMANCE"

class ParametreSysteme(Base):
    """Modèle représentant un paramètre système"""
    __tablename__ = "parametres_systeme"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    description = Column(String(500))
    type_parametre = Column(Enum(TypeParametre), nullable=False)
    valeur = Column(JSON, nullable=False)  # Valeur du paramètre (peut être de n'importe quel type)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules_systeme.id"))
    actif = Column(Boolean, default=True)
    metadata_config = Column(JSON)  # Métadonnées de configuration (validation, etc.)

    # Relations
    module = relationship("ModuleSysteme", back_populates="parametres")
