from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime, Enum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from models.base import BaseModel

class PrioriteTache(str, PyEnum):
    """Énumération des niveaux de priorité des tâches"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class StatutTache(str, PyEnum):
    """Énumération des statuts des tâches"""
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_ATTENTE = "EN_ATTENTE"
    TERMINEE = "TERMINEE"
    ANNULEE = "ANNULEE"

class CategorieTache(str, PyEnum):
    """Énumération des catégories de tâches"""
    PRODUCTION = "PRODUCTION"
    MAINTENANCE = "MAINTENANCE"
    RECOLTE = "RECOLTE"
    PLANTATION = "PLANTATION"
    IRRIGATION = "IRRIGATION"
    TRAITEMENT = "TRAITEMENT"
    AUTRE = "AUTRE"

class Tache(BaseModel):
    """Modèle pour les tâches du projet"""
    __tablename__ = "taches"

    titre = Column(String(200), nullable=False)
    description = Column(String(1000))
    statut = Column(Enum(StatutTache), default=StatutTache.A_FAIRE, nullable=False)
    priorite = Column(Enum(PrioriteTache), default=PrioriteTache.MOYENNE, nullable=False)
    categorie = Column(Enum(CategorieTache), default=CategorieTache.AUTRE, nullable=False)
    
    # Dates
    date_debut = Column(DateTime(timezone=True))
    date_fin_prevue = Column(DateTime(timezone=True))
    date_fin_reelle = Column(DateTime(timezone=True))
    
    # Relations
    projet_id = Column(UUID(as_uuid=True), ForeignKey("projets.id"), nullable=False)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"))
    
    # Météo
    dependant_meteo = Column(Boolean, default=False)
    min_temperature = Column(Float)  # Température minimale requise
    max_temperature = Column(Float)  # Température maximale acceptable
    max_wind_speed = Column(Float)   # Vitesse du vent maximale acceptable
    max_precipitation = Column(Float) # Précipitations maximales acceptables
    
    # Progression
    heures_estimees = Column(Float)
    heures_reelles = Column(Float)
    pourcentage_completion = Column(Integer, default=0)
    
    # Relations bidirectionnelles
    responsable = relationship("Employe", back_populates="taches_assignees")
    parcelle = relationship("Parcelle", back_populates="taches")
    ressources = relationship("RessourceTache", back_populates="tache")
    commentaires = relationship("CommentaireTache", back_populates="tache")
    dependances = relationship(
        "DependanceTache",
        primaryjoin="or_(Tache.id==DependanceTache.tache_id, Tache.id==DependanceTache.dependance_id)"
    )

class RessourceTache(BaseModel):
    """Modèle pour les ressources assignées aux tâches"""
    __tablename__ = "ressources_tache"

    tache_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"), nullable=False)
    ressource_id = Column(UUID(as_uuid=True), ForeignKey("ressources.id"), nullable=False)
    quantite_requise = Column(Float, nullable=False)
    quantite_utilisee = Column(Float, default=0)
    
    tache = relationship("Tache", back_populates="ressources")
    ressource = relationship("Resource", back_populates="utilisations_tache")

class CommentaireTache(BaseModel):
    """Modèle pour les commentaires sur les tâches"""
    __tablename__ = "commentaires_tache"

    tache_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"), nullable=False)
    auteur_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    contenu = Column(String(1000), nullable=False)
    
    tache = relationship("Tache", back_populates="commentaires")
    auteur = relationship("Employe", back_populates="commentaires_tache")

class DependanceTache(BaseModel):
    """Modèle pour les dépendances entre tâches"""
    __tablename__ = "dependances_tache"

    tache_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"), nullable=False)
    dependance_id = Column(UUID(as_uuid=True), ForeignKey("taches.id"), nullable=False)
    type_dependance = Column(String(50), default="fin_vers_debut")  # fin_vers_debut, debut_vers_debut, etc.
    
    tache = relationship("Tache", foreign_keys=[tache_id])
    dependance = relationship("Tache", foreign_keys=[dependance_id])

# Définition de la relation après la définition de la classe Project
from models.project import Project
Tache.projet = relationship("Project", back_populates="taches")