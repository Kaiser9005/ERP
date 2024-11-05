from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from ..base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class CultureType(str, enum.Enum):
    """Types de cultures disponibles"""
    PALMIER = "PALMIER"
    PAPAYE = "PAPAYE"

class ParcelleStatus(str, enum.Enum):
    """Statuts possibles d'une parcelle"""
    ACTIVE = "ACTIVE"
    EN_REPOS = "EN_REPOS"
    EN_PREPARATION = "EN_PREPARATION"

class Parcelle(Base):
    """Modèle représentant une parcelle agricole"""
    __tablename__ = "parcelles"

    code = Column(String(50), unique=True, index=True, nullable=False)
    culture_type = Column(Enum(CultureType), nullable=False)
    surface_hectares = Column(Numeric(10, 2), nullable=False)
    date_plantation = Column(Date, nullable=False)
    statut = Column(Enum(ParcelleStatus), default=ParcelleStatus.EN_PREPARATION)
    coordonnees_gps = Column(JSON)  # {latitude: float, longitude: float}
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    metadata = Column(JSON)  # Données supplémentaires

    # Relations
    responsable = relationship("Employe", back_populates="parcelles_gerees")
    cycles_culture = relationship("CycleCulture", back_populates="parcelle")
    recoltes = relationship("Recolte", back_populates="parcelle")

class CycleCulture(Base):
    """Modèle représentant un cycle de culture"""
    __tablename__ = "cycles_culture"

    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date)
    rendement_prevu = Column(Numeric(10, 2))  # en kg/hectare
    rendement_reel = Column(Numeric(10, 2))
    notes = Column(Text)
    metadata = Column(JSON)  # Données supplémentaires (traitements, observations, etc.)

    # Relations
    parcelle = relationship("Parcelle", back_populates="cycles_culture")

class QualiteRecolte(str, enum.Enum):
    """Niveaux de qualité des récoltes"""
    A = "A"  # Qualité supérieure
    B = "B"  # Qualité standard
    C = "C"  # Qualité inférieure

class Recolte(Base):
    """Modèle représentant une récolte"""
    __tablename__ = "recoltes"

    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"), nullable=False)
    date_recolte = Column(DateTime, nullable=False)
    quantite_kg = Column(Numeric(10, 2), nullable=False)
    qualite = Column(Enum(QualiteRecolte), nullable=False)
    equipe_recolte = Column(JSON)  # Liste des IDs des employés
    conditions_meteo = Column(JSON)  # {temperature: float, humidite: float, precipitation: float}
    notes = Column(Text)
    metadata = Column(JSON)  # Données supplémentaires

    # Relations
    parcelle = relationship("Parcelle", back_populates="recoltes")

    @property
    def rendement_hectare(self):
        """Calcule le rendement par hectare"""
        if self.parcelle and self.parcelle.surface_hectares:
            return self.quantite_kg / self.parcelle.surface_hectares
        return None
