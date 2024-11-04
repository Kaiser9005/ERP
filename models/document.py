from sqlalchemy import Column, String, Enum, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class TypeDocument(str, enum.Enum):
    """Types de documents"""
    CONTRAT = "CONTRAT"
    FACTURE = "FACTURE"
    BON_LIVRAISON = "BON_LIVRAISON"
    PIECE_JOINTE = "PIECE_JOINTE"
    RAPPORT = "RAPPORT"
    AUTRE = "AUTRE"

class Document(Base):
    """Modèle représentant un document"""
    __tablename__ = "documents"

    nom = Column(String(200), nullable=False)
    type_document = Column(Enum(TypeDocument), nullable=False)
    description = Column(Text)
    chemin_fichier = Column(String(500), nullable=False)
    taille = Column(Integer)  # Taille en octets
    type_mime = Column(String(100))
    metadata = Column(JSON)  # Métadonnées additionnelles
    module = Column(String(50))  # Module associé (finance, rh, etc.)
    reference_id = Column(UUID(as_uuid=True))  # ID de l'objet associé
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    uploaded_by = relationship("Employe")