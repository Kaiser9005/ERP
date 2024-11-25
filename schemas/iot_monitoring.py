"""Schémas de validation pour le monitoring IoT."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field

from models.iot_sensor import SensorType, SensorStatus

class SensorHealthSchema(BaseModel):
    """État de santé d'un capteur."""
    id: UUID
    code: str
    type: SensorType
    status: SensorStatus
    message: str
    batterie: Optional[float]
    signal: Optional[float]
    derniere_lecture: Optional[datetime]

class SensorReadingStatsSchema(BaseModel):
    """Statistiques des lectures d'un capteur."""
    moyenne: float
    minimum: float
    maximum: float
    nombre_lectures: int

class SensorReadingsSchema(BaseModel):
    """Lectures agrégées d'un capteur."""
    capteur_id: UUID
    lectures: List[Dict[str, Any]]
    statistiques: SensorReadingStatsSchema

class SensorAlertSchema(BaseModel):
    """Alerte d'un capteur."""
    capteur_id: UUID
    type: str
    valeur: Optional[float]
    seuil: Optional[float]
    timestamp: datetime
    message: str
    status: Optional[SensorStatus]

class MLPredictionSchema(BaseModel):
    """Prédiction ML pour une parcelle."""
    type_capteur: SensorType
    predictions: List[Dict[str, Any]]
    confiance: float
    facteurs_influence: List[str]
    recommandations: List[str]

class SystemHealthSchema(BaseModel):
    """État de santé global du système IoT."""
    total_capteurs: int
    capteurs_actifs: int
    capteurs_maintenance: int
    capteurs_erreur: int
    batterie_faible: int
    signal_faible: int
    sante_globale: float
    timestamp: datetime

class MaintenanceRecommendationSchema(BaseModel):
    """Recommandation de maintenance pour un capteur."""
    capteur_id: UUID
    code: str
    type: SensorType
    priorite: str
    raison: str
    action_recommandee: str
    deadline: datetime

class MonitoringDataSchema(BaseModel):
    """Données complètes de monitoring pour une parcelle."""
    parcelle_id: UUID
    periode: Dict[str, datetime]
    capteurs: List[SensorHealthSchema]
    mesures: Dict[SensorType, List[SensorReadingsSchema]]
    alertes: List[SensorAlertSchema]
    predictions: Dict[str, Any]
    sante_systeme: SystemHealthSchema

class MonitoringDashboardSchema(BaseModel):
    """Données pour le dashboard de monitoring."""
    temps_reel: MonitoringDataSchema
    historique: Dict[str, MonitoringDataSchema]
    predictions: Dict[str, MLPredictionSchema]
    maintenance: List[MaintenanceRecommendationSchema]

# Schémas pour les requêtes
class MonitoringRequestSchema(BaseModel):
    """Paramètres pour une requête de monitoring."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    types_capteur: Optional[List[SensorType]] = None
    inclure_predictions: bool = True
    inclure_maintenance: bool = True

class MaintenanceRequestSchema(BaseModel):
    """Paramètres pour une requête de maintenance."""
    priorite_minimum: Optional[str] = None
    types_capteur: Optional[List[SensorType]] = None
    deadline_max: Optional[datetime] = None

# Schémas pour les réponses d'erreur
class MonitoringErrorSchema(BaseModel):
    """Erreur lors du monitoring."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Schémas pour les webhooks
class SensorAlertWebhookSchema(BaseModel):
    """Données pour le webhook d'alerte capteur."""
    type_alerte: str
    capteur_id: UUID
    message: str
    timestamp: datetime
    niveau: str
    donnees: Dict[str, Any]

class MaintenanceAlertWebhookSchema(BaseModel):
    """Données pour le webhook d'alerte maintenance."""
    capteur_id: UUID
    type_maintenance: str
    priorite: str
    deadline: datetime
    description: str
    actions_requises: List[str]

# Schémas pour la configuration
class MonitoringConfigSchema(BaseModel):
    """Configuration du monitoring."""
    intervalle_actualisation: int = 300  # secondes
    seuil_alerte_batterie: float = 20.0  # pourcentage
    seuil_alerte_signal: float = 30.0    # pourcentage
    periode_retention_donnees: int = 90   # jours
    webhook_urls: Dict[str, str] = Field(default_factory=dict)
    notifications_email: List[str] = Field(default_factory=list)
