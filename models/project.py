import enum
import uuid
from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base, BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID


class ProjectStatus(enum.Enum):
    """Statuts possibles d'un projet"""
    PLANIFIE = "PLANIFIE"
    EN_COURS = "EN_COURS"
    EN_PAUSE = "EN_PAUSE"
    TERMINE = "TERMINE"
    ANNULE = "ANNULE"

class Project(Base):
    """Modèle représentant un projet"""
    __tablename__ = "projets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, index=True, nullable=False)
    nom = Column(String(200), nullable=False)
    description = Column(Text)
    date_debut = Column(Date, nullable=False)
    date_fin_prevue = Column(Date, nullable=False)
    date_fin_reelle = Column(Date)
    statut = Column(Enum(ProjectStatus), default=ProjectStatus.PLANIFIE)    
    budget = Column(Numeric(10, 2))
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    objectifs = Column(JSON)  # Liste des objectifs du projet
    risques = Column(JSON)  # Liste des risques identifiés
    
    # Relations
    responsable = relationship("Employe", back_populates="projets_geres")
    taches = relationship("Tache", back_populates="projet")
    documents = relationship("ProjectDocument", back_populates="projet")

class ProjectDocument(BaseModel):
    """Modèle représentant un document lié à un projet"""
    __tablename__ = "documents_projet"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    nom = Column(String(200), nullable=False)
    type = Column(String(50))  # Type de document (contrat, rapport, etc.)
    chemin_fichier = Column(String(500), nullable=False)  # Chemin vers le fichier
    date_upload = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), nullable=False)
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    projet = relationship("Project", back_populates="documents")
    uploaded_by = relationship("Employe")
