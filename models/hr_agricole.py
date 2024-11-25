"""
Modèles spécifiques pour la gestion RH agricole
"""

from sqlalchemy import Column, String, Enum, JSON, ForeignKey, Text, Date, DateTime, Boolean, Numeric, Integer
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TypePersonnel(str, enum.Enum):
    """Types de personnel agricole"""
    PERMANENT = "PERMANENT"
    SAISONNIER = "SAISONNIER"
    TEMPORAIRE = "TEMPORAIRE"
    STAGIAIRE = "STAGIAIRE"

class SpecialiteAgricole(str, enum.Enum):
    """Spécialités agricoles"""
    CULTURE = "CULTURE"
    ELEVAGE = "ELEVAGE"
    MARAICHAGE = "MARAICHAGE"
    ARBORICULTURE = "ARBORICULTURE"
    MAINTENANCE = "MAINTENANCE"
    LOGISTIQUE = "LOGISTIQUE"

class NiveauCompetence(str, enum.Enum):
    """Niveaux de compétence"""
    DEBUTANT = "DEBUTANT"
    INTERMEDIAIRE = "INTERMEDIAIRE"
    AVANCE = "AVANCE"
    EXPERT = "EXPERT"

class TypeCertification(str, enum.Enum):
    """Types de certifications agricoles"""
    PHYTOSANITAIRE = "PHYTOSANITAIRE"
    SECURITE = "SECURITE"
    CONDUITE_ENGINS = "CONDUITE_ENGINS"
    BIO = "BIO"
    QUALITE = "QUALITE"

class CompetenceAgricole(Base):
    """Modèle représentant une compétence agricole"""
    __tablename__ = "competences_agricoles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    specialite = Column(Enum(SpecialiteAgricole), nullable=False)
    niveau = Column(Enum(NiveauCompetence), nullable=False)
    cultures = Column(JSON)  # Liste des cultures maîtrisées
    equipements = Column(JSON)  # Liste des équipements maîtrisés
    date_acquisition = Column(Date, nullable=False)
    date_mise_a_jour = Column(Date)
    validite = Column(Date)  # Date d'expiration si applicable
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="competences_agricoles")
    certifications = relationship("CertificationAgricole", back_populates="competence")

class CertificationAgricole(Base):
    """Modèle représentant une certification agricole"""
    __tablename__ = "certifications_agricoles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    competence_id = Column(UUID(as_uuid=True), ForeignKey("competences_agricoles.id"), nullable=False)
    type_certification = Column(Enum(TypeCertification), nullable=False)
    organisme = Column(String(100), nullable=False)
    numero = Column(String(50))
    date_obtention = Column(Date, nullable=False)
    date_expiration = Column(Date)
    niveau = Column(String(50))
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    competence = relationship("CompetenceAgricole", back_populates="certifications")
    document = relationship("Document")

class AffectationParcelle(Base):
    """Modèle représentant une affectation à une parcelle"""
    __tablename__ = "affectations_parcelles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date)
    role = Column(String(100), nullable=False)
    responsabilites = Column(JSON)  # Liste des responsabilités
    objectifs = Column(JSON)  # Objectifs spécifiques
    restrictions_meteo = Column(JSON)  # Conditions météo limitantes
    equipements_requis = Column(JSON)  # Équipements nécessaires
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="affectations_parcelles")
    parcelle = relationship("Parcelle")

class ConditionTravailAgricole(Base):
    """Modèle représentant les conditions de travail agricole"""
    __tablename__ = "conditions_travail_agricoles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    date = Column(Date, nullable=False)
    temperature = Column(Numeric(4, 1))  # °C
    humidite = Column(Integer)  # %
    precipitation = Column(Boolean, default=False)
    vent = Column(Numeric(4, 1))  # km/h
    exposition_soleil = Column(Integer)  # minutes
    charge_physique = Column(Integer)  # 1-10
    equipements_protection = Column(JSON)  # Liste des EPI utilisés
    incidents = Column(JSON)  # Incidents éventuels
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="conditions_travail")

class FormationAgricole(Base):
    """Modèle représentant une formation agricole spécifique"""
    __tablename__ = "formations_agricoles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    formation_id = Column(UUID(as_uuid=True), ForeignKey("formations.id"), nullable=False)
    specialite = Column(Enum(SpecialiteAgricole), nullable=False)
    cultures_concernees = Column(JSON)  # Liste des cultures
    equipements_concernes = Column(JSON)  # Liste des équipements
    conditions_meteo = Column(JSON)  # Conditions météo couvertes
    pratiques_specifiques = Column(JSON)  # Pratiques agricoles enseignées
    evaluation_terrain = Column(Boolean, default=False)
    resultats_evaluation = Column(JSON)
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    formation = relationship("Formation", back_populates="details_agricoles")

class EvaluationAgricole(Base):
    """Modèle représentant une évaluation agricole spécifique"""
    __tablename__ = "evaluations_agricoles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("evaluations.id"), nullable=False)
    performances_cultures = Column(JSON)  # Performances par culture
    maitrise_equipements = Column(JSON)  # Maîtrise des équipements
    respect_securite = Column(JSON)  # Respect des consignes
    adaptabilite_meteo = Column(JSON)  # Adaptation conditions météo
    gestion_ressources = Column(JSON)  # Gestion des ressources
    qualite_travail = Column(JSON)  # Qualité du travail
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    evaluation = relationship("Evaluation", back_populates="details_agricoles")
