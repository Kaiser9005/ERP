"""Schémas Pydantic pour le monitoring IoT."""

from datetime import datetime
from typing import Optional, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field

from models.iot_sensor import SensorType, SensorStatus

class IoTSensorCreate(BaseModel):
    """Schéma pour la création d'un capteur."""
    code: str
    type: SensorType
    parcelle_id: UUID
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    config: Dict = Field(default_factory=dict)
    seuils_alerte: Dict = Field(default_factory=dict)
    intervalle_lecture: float = 300
    fabricant: Optional[str] = None
    modele: Optional[str] = None
    firmware: Optional[str] = None

class IoTSensorUpdate(BaseModel):
    """Schéma pour la mise à jour d'un capteur."""
    status: Optional[SensorStatus]
    config: Optional[Dict]
    seuils_alerte: Optional[Dict]
    intervalle_lecture: Optional[float]
    firmware: Optional[str]
    derniere_maintenance: Optional[datetime]
    prochaine_maintenance: Optional[datetime]

class SensorReadingCreate(BaseModel):
    """Schéma pour la création d'une lecture de capteur."""
    valeur: float
    unite: str
    qualite_signal: Optional[float] = None
    niveau_batterie: Optional[float] = None
    meta_data: Dict = Field(default_factory=dict)

class MonitoringRequestSchema(BaseModel):
    """Schéma pour une requête de monitoring."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: List[str] = Field(default_factory=list)
    aggregation: Optional[str] = "hour"

class MonitoringDataPoint(BaseModel):
    """Point de données de monitoring."""
    timestamp: datetime
    value: float
    unit: str
    quality: Optional[float] = None

class MonitoringDataSeries(BaseModel):
    """Série de données de monitoring."""
    sensor_id: UUID
    sensor_type: SensorType
    metric: str
    data: List[MonitoringDataPoint]

class MonitoringDataSchema(BaseModel):
    """Schéma pour les données de monitoring."""
    parcelle_id: UUID
    period_start: datetime
    period_end: datetime
    series: List[MonitoringDataSeries]
    metadata: Dict = Field(default_factory=dict)

class MonitoringStatsSchema(BaseModel):
    """Statistiques de monitoring."""
    min_value: float
    max_value: float
    avg_value: float
    std_dev: Optional[float] = None
    samples_count: int

class MonitoringDashboardSchema(BaseModel):
    """Schéma pour le dashboard de monitoring."""
    parcelle_id: UUID
    timestamp: datetime
    sensors_status: Dict[UUID, SensorStatus]
    current_values: Dict[UUID, MonitoringDataPoint]
    daily_stats: Dict[UUID, MonitoringStatsSchema]
    alerts_count: int
    maintenance_due: List[UUID]

class MaintenanceRequestSchema(BaseModel):
    """Schéma pour une requête de maintenance."""
    sensor_ids: Optional[List[UUID]] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class MaintenanceRecommendationSchema(BaseModel):
    """Schéma pour une recommandation de maintenance."""
    sensor_id: UUID
    sensor_type: SensorType
    priority: str
    reason: str
    recommended_date: datetime
    estimated_duration: int  # minutes
    required_skills: List[str]
    parts_needed: Optional[List[str]] = None

class MonitoringConfigSchema(BaseModel):
    """Configuration du monitoring."""
    sampling_interval: int = 300  # secondes
    alert_thresholds: Dict[str, Dict[str, float]]
    maintenance_intervals: Dict[str, int]  # jours
    data_retention: int = 365  # jours
    aggregation_policies: Dict[str, str]

class MonitoringErrorSchema(BaseModel):
    """Schéma pour les erreurs de monitoring."""
    code: str
    message: str
    details: Optional[Dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SensorAlertWebhookSchema(BaseModel):
    """Schéma pour les webhooks d'alertes."""
    sensor_id: UUID
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    value: Optional[float] = None
    threshold: Optional[float] = None
    metadata: Dict = Field(default_factory=dict)
