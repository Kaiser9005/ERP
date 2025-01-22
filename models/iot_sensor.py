"""Module de gestion des capteurs IoT pour le monitoring agricole."""

from datetime import datetime
import uuid
import enum
from dataclasses import dataclass
from typing import Optional, Dict, Any
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

@dataclass
class SensorData:
    """Structure de données pour les mesures des capteurs."""
    capteur_id: str
    type: SensorType
    valeur: float
    unite: str
    timestamp: datetime
    qualite_signal: Optional[float] = None
    niveau_batterie: Optional[float] = None
    meta_data: Optional[Dict[str, Any]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertit les données en dictionnaire."""
        return {
            "capteur_id": self.capteur_id,
            "type": self.type.value,
            "valeur": self.valeur,
            "unite": self.unite,
            "timestamp": self.timestamp.isoformat(),
            "qualite_signal": self.qualite_signal,
            "niveau_batterie": self.niveau_batterie,
            "meta_data": self.meta_data or {},
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SensorData':
        """Crée une instance à partir d'un dictionnaire."""
        return cls(
            capteur_id=data["capteur_id"],
            type=SensorType(data["type"]),
            valeur=float(data["valeur"]),
            unite=data["unite"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"],
            qualite_signal=float(data["qualite_signal"]) if data.get("qualite_signal") is not None else None,
            niveau_batterie=float(data["niveau_batterie"]) if data.get("niveau_batterie") is not None else None,
            meta_data=data.get("meta_data", {}),
            latitude=float(data["latitude"]) if data.get("latitude") is not None else None,
            longitude=float(data["longitude"]) if data.get("longitude") is not None else None,
            altitude=float(data["altitude"]) if data.get("altitude") is not None else None
        )

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

    def to_sensor_data(self) -> SensorData:
        """Convertit la lecture en SensorData."""
        return SensorData(
            capteur_id=str(self.capteur_id),
            type=self.capteur.type,
            valeur=self.valeur,
            unite=self.unite,
            timestamp=self.timestamp,
            qualite_signal=self.qualite_signal,
            niveau_batterie=self.niveau_batterie,
            meta_data=self.meta_data,
            latitude=self.capteur.latitude,
            longitude=self.capteur.longitude,
            altitude=self.capteur.altitude
        )
