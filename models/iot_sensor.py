"""Module de gestion des capteurs IoT pour le monitoring agricole."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base

class SensorType(str, enum.Enum):
    """Types de capteurs supportés."""
    TEMPERATURE_SOL = "temperature_sol"
    TEMPERATURE_AIR = "temperature_air"
    HUMIDITE_SOL = "humidite_sol"
    HUMIDITE_AIR = "humidite_air"
    LUMINOSITE = "luminosite"
    PLUVIOMETRIE = "pluviometrie"
    PH_SOL = "ph_sol"
    CONDUCTIVITE = "conductivite"

class SensorStatus(str, enum.Enum):
    """États possibles d'un capteur."""
    ACTIF = "actif"
    INACTIF = "inactif"
    MAINTENANCE = "maintenance"
    ERREUR = "erreur"

class IoTSensor(Base):
    """Modèle de données pour les capteurs IoT."""
    __tablename__ = "iot_sensors"

    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(String, unique=True, nullable=False)
    type = Column(Enum(SensorType), nullable=False)
    status = Column(Enum(SensorStatus), default=SensorStatus.ACTIF)
    
    # Localisation
    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    
    # Configuration
    config = Column(JSON, default={})
    seuils_alerte = Column(JSON, default={})
    intervalle_lecture = Column(Float, default=300)  # en secondes
    
    # Métadonnées
    fabricant = Column(String)
    modele = Column(String)
    firmware = Column(String)
    date_installation = Column(DateTime, default=datetime.utcnow)
    derniere_maintenance = Column(DateTime)
    prochaine_maintenance = Column(DateTime)
    
    # Relations
    parcelle = relationship("Parcelle", back_populates="capteurs")
    lectures = relationship("SensorReading", back_populates="capteur")

class SensorReading(Base):
    """Modèle de données pour les lectures des capteurs."""
    __tablename__ = "sensor_readings"

    id = Column(UUID(as_uuid=True), primary_key=True)
    capteur_id = Column(UUID(as_uuid=True), ForeignKey("iot_sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    valeur = Column(Float, nullable=False)
    unite = Column(String, nullable=False)
    qualite_signal = Column(Float)  # 0-100%
    niveau_batterie = Column(Float)  # 0-100%
    metadata = Column(JSON, default={})
    
    # Relations
    capteur = relationship("IoTSensor", back_populates="lectures")

# Schémas Pydantic pour l'API
class SensorReadingCreate(BaseModel):
    """Schéma pour la création d'une lecture de capteur."""
    valeur: float
    unite: str
    qualite_signal: Optional[float] = None
    niveau_batterie: Optional[float] = None
    metadata: dict = Field(default_factory=dict)

class SensorReading(BaseModel):
    """Schéma pour la lecture d'un capteur."""
    id: UUID
    capteur_id: UUID
    timestamp: datetime
    valeur: float
    unite: str
    qualite_signal: Optional[float]
    niveau_batterie: Optional[float]
    metadata: dict

    class Config:
        orm_mode = True

class IoTSensorCreate(BaseModel):
    """Schéma pour la création d'un capteur."""
    code: str
    type: SensorType
    parcelle_id: UUID
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    config: dict = Field(default_factory=dict)
    seuils_alerte: dict = Field(default_factory=dict)
    intervalle_lecture: float = 300
    fabricant: Optional[str] = None
    modele: Optional[str] = None
    firmware: Optional[str] = None

class IoTSensor(BaseModel):
    """Schéma pour un capteur."""
    id: UUID
    code: str
    type: SensorType
    status: SensorStatus
    parcelle_id: UUID
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[float]
    config: dict
    seuils_alerte: dict
    intervalle_lecture: float
    fabricant: Optional[str]
    modele: Optional[str]
    firmware: Optional[str]
    date_installation: datetime
    derniere_maintenance: Optional[datetime]
    prochaine_maintenance: Optional[datetime]

    class Config:
        orm_mode = True

class IoTSensorUpdate(BaseModel):
    """Schéma pour la mise à jour d'un capteur."""
    status: Optional[SensorStatus]
    config: Optional[dict]
    seuils_alerte: Optional[dict]
    intervalle_lecture: Optional[float]
    firmware: Optional[str]
    derniere_maintenance: Optional[datetime]
    prochaine_maintenance: Optional[datetime]
