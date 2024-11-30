"""Module de gestion des capteurs IoT pour le monitoring agricole."""

from datetime import datetime
import uuid
import enum
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    type = Column(Enum(SensorType), nullable=False)
    status = Column(Enum(SensorStatus), default=SensorStatus.ACTIF)
    
    # Localisation
    parcelle_id = Column(UUID, ForeignKey("parcelles.id"))
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

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    capteur_id = Column(UUID, ForeignKey("iot_sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    valeur = Column(Float, nullable=False)
    unite = Column(String, nullable=False)
    qualite_signal = Column(Float)  # 0-100%
    niveau_batterie = Column(Float)  # 0-100%
    meta_data = Column(JSON, default={})  # Renommé de metadata à meta_data
    
    # Relations
    capteur = relationship("IoTSensor", back_populates="lectures")
