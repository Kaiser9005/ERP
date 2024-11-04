from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base
import enum
from datetime import datetime

class TypeNotification(str, enum.Enum):
    """Types de notifications système"""
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

class ModuleNotification(str, enum.Enum):
    """Modules sources des notifications"""
    SYSTEME = "SYSTEME"
    PRODUCTION = "PRODUCTION"
    INVENTAIRE = "INVENTAIRE"
    RH = "RH"
    FINANCE = "FINANCE"

class Notification(Base):
    """Modèle pour les notifications système"""
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True)
    titre = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(Enum(TypeNotification), nullable=False)
    module = Column(Enum(ModuleNotification), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    lu = Column(Boolean, default=False)
    destinataire_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    lien = Column(String(200))  # Lien optionnel vers une ressource
    donnees = Column(JSON)  # Données supplémentaires

    # Relations
    destinataire = relationship("Utilisateur", back_populates="notifications")