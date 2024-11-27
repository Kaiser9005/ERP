from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship

from models.base import Base
from models.hr import Employee

class Formation(Base):
    """Modèle pour les formations des employés"""
    __tablename__ = "formations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    titre = Column(String(100), nullable=False)
    description = Column(String(500))
    type = Column(String(50), nullable=False)  # 'technique', 'securite', 'agricole'
    duree = Column(Integer, nullable=False)  # En heures
    competences_requises = Column(JSON)
    competences_acquises = Column(JSON)
    materiel_requis = Column(JSON)
    conditions_meteo = Column(JSON)  # Conditions météo requises/restrictions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SessionFormation(Base):
    """Modèle pour les sessions de formation"""
    __tablename__ = "sessions_formation"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    formation_id = Column(String(36), ForeignKey("formations.id"), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    lieu = Column(String(100))
    formateur = Column(String(100))
    statut = Column(String(20), default="planifie")  # planifie, en_cours, termine, annule
    nb_places = Column(Integer)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    formation = relationship("Formation", backref="sessions")

class ParticipationFormation(Base):
    """Modèle pour la participation des employés aux formations"""
    __tablename__ = "participations_formation"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(String(36), ForeignKey("sessions_formation.id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.id"), nullable=False)
    statut = Column(String(20), default="inscrit")  # inscrit, present, absent, complete
    note = Column(Integer)  # Note sur 100
    commentaires = Column(String(500))
    certification_obtenue = Column(Boolean, default=False)
    date_certification = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("SessionFormation", backref="participations")
    employee = relationship("Employee", backref="participations_formations")

class Evaluation(Base):
    """Modèle pour les évaluations des employés"""
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    employee_id = Column(String(36), ForeignKey("employees.id"), nullable=False)
    evaluateur_id = Column(String(36), ForeignKey("employees.id"), nullable=False)
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

    employee = relationship("Employee", foreign_keys=[employee_id], backref="evaluations_recues")
    evaluateur = relationship("Employee", foreign_keys=[evaluateur_id], backref="evaluations_donnees")
