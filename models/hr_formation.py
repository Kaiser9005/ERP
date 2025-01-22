from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base
from models.hr import Employe

class Formation(Base):
    """Modèle pour les formations"""
    __tablename__ = "formations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    description = Column(String(500))
    type = Column(String(50), nullable=False)  # technique, securite, management, qualite, autre
    duree = Column(Integer)  # en heures
    prerequis = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    # Relations
    participations = relationship("ParticipationFormation", back_populates="formation")
    details_agricoles = relationship("FormationAgricole", back_populates="formation", uselist=False)
    sessions = relationship("SessionFormation", back_populates="formation")

class SessionFormation(Base):
    """Modèle pour les sessions de formation"""
    __tablename__ = "sessions_formation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    formation_id = Column(UUID(as_uuid=True), ForeignKey("formations.id"), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    lieu = Column(String(100))
    formateur = Column(String(100))
    statut = Column(String(20), default="planifie")  # planifie, en_cours, termine, annule
    nb_places = Column(Integer)
    notes = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    # Relations
    formation = relationship("Formation", back_populates="sessions")
    participations = relationship("ParticipationFormation", back_populates="session")

class ParticipationFormation(Base):
    """Modèle pour la participation des employés aux formations"""
    __tablename__ = "participations_formation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    formation_id = Column(UUID(as_uuid=True), ForeignKey("formations.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions_formation.id"), nullable=False)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    statut = Column(String(20), default="inscrit")  # inscrit, present, absent, complete
    note = Column(Integer)  # Note sur 100
    commentaires = Column(String(500))
    certification_obtenue = Column(Boolean, default=False)
    date_certification = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    formation = relationship("Formation", back_populates="participations")
    session = relationship("SessionFormation", back_populates="participations")
    employe = relationship("Employe", back_populates="participations_formations")

class Evaluation(Base):
    """Modèle pour les évaluations des employés"""
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    evaluateur_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    date_evaluation = Column(DateTime, nullable=False)
    type = Column(String(50), nullable=False)  # periodique, formation, projet
    periode_debut = Column(DateTime)
    periode_fin = Column(DateTime)
    competences = Column(JSON)  # Évaluation des compétences
    objectifs = Column(JSON)  # Objectifs fixés/atteints
    performances = Column(JSON)  # Métriques de performance
    points_forts = Column(String(500))
    points_amelioration = Column(String(500))
    plan_action = Column(String(500))
    note_globale = Column(Integer)  # Note sur 100
    statut = Column(String(20), default="brouillon")  # brouillon, valide, archive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    employe = relationship("Employe", foreign_keys=[employe_id], back_populates="evaluations_recues")
    evaluateur = relationship("Employe", foreign_keys=[evaluateur_id], back_populates="evaluations_donnees")
    details_agricoles = relationship("EvaluationAgricole", back_populates="evaluation", uselist=False)

class ThemeFormation(Base):
    """Modèle pour les thèmes de formation"""
    __tablename__ = "themes_formation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))
