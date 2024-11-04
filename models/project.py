from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class ProjectStatus(str, enum.Enum):
    """Statuts possibles d'un projet"""
    PLANIFIE = "PLANIFIE"
    EN_COURS = "EN_COURS"
    EN_PAUSE = "EN_PAUSE"
    TERMINE = "TERMINE"
    ANNULE = "ANNULE"

class TaskPriority(str, enum.Enum):
    """Niveaux de priorité des tâches"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class TaskStatus(str, enum.Enum):
    """Statuts possibles d'une tâche"""
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_REVUE = "EN_REVUE"
    TERMINE = "TERMINE"
    BLOQUE = "BLOQUE"

class Project(Base):
    """Modèle représentant un projet"""
    __tablename__ = "projets"

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
    taches = relationship("Task", back_populates="projet")
    documents = relationship("ProjectDocument", back_populates="projet")

class Task(Base):
    """Modèle représentant une tâche de projet"""
    __tablename__ = "taches"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    priorite = Column(Enum(TaskPriority), default=TaskPriority.MOYENNE)
    statut = Column(Enum(TaskStatus), default=TaskStatus.A_FAIRE)
    date_debut = Column(DateTime)
    date_fin_prevue = Column(DateTime, nullable=False)
    date_fin_reelle = Column(DateTime)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    temps_estime = Column(Numeric(5, 2))  # En heures
    temps_passe = Column(Numeric(5, 2))  # En heures
    dependances = Column(JSON)  # Liste des IDs des tâches dont celle-ci dépend
    
    # Relations
    projet = relationship("Project", back_populates="taches")
    assignee = relationship("Employe", back_populates="taches_assignees")
    commentaires = relationship("TaskComment", back_populates="tache")

class TaskComment(Base):
    """Modèle représentant un commentaire sur une tâche"""
    __tablename__ = "commentaires_tache"

    tache_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"), nullable=False)
    auteur_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    contenu = Column(Text, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    tache = relationship("Task", back_populates="commentaires")
    auteur = relationship("Employe")

class ProjectDocument(Base):
    """Modèle représentant un document lié à un projet"""
    __tablename__ = "documents_projet"

    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    nom = Column(String(200), nullable=False)
    type = Column(String(50))  # Type de document (contrat, rapport, etc.)
    chemin_fichier = Column(String(500), nullable=False)  # Chemin vers le fichier
    date_upload = Column(DateTime, default=datetime.utcnow, nullable=False)
    uploaded_by_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    
    # Relations
    projet = relationship("Project", back_populates="documents")
    uploaded_by = relationship("Employe")