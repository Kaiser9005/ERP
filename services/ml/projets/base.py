"""Service de base pour l'apprentissage automatique des projets."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from models.tache import Tache as Task, StatutTache as TaskStatus  # Renommé pour utiliser les noms français
from models.resource import Resource, ResourceType
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService

class ProjectsMLService:
    """Service ML pour l'optimisation des projets agricoles."""
    
    def __init__(self, db: Session):
        """Initialisation du service."""
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        self.cache = CacheService()
        
        # Initialisation du modèle ML
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )

    async def _get_project_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les tâches d'un projet."""
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        return [{
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "progress": task.progress,
            "dependencies": task.dependencies,
            "resources": task.resources,
            "metrics": task.metrics,
            "weather_sensitive": task.weather_sensitive,
            "weather_conditions": task.weather_conditions
        } for task in tasks]

    async def _get_project_resources(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les ressources d'un projet."""
        resources = self.db.query(Resource).filter(
            Resource.project_id == project_id
        ).all()
        return [{
            "id": resource.id,
            "type": resource.type,
            "name": resource.name,
            "availability": resource.availability,
            "efficiency": resource.efficiency,
            "cost": float(resource.cost)
        } for resource in resources]

    async def _get_iot_data(self, project_id: str) -> Dict[str, Any]:
        """Récupère les données IoT d'un projet."""
        sensors = await self.iot_service.get_sensors_by_parcelle(project_id)
        
        sensor_data = {}
        for sensor in sensors:
            readings = await self.iot_service.get_sensor_readings(
                sensor.id,
                start_date=datetime.now(datetime.timezone.utc) - timedelta(days=7)  # Utilisation de timezone.utc
            )
            
            stats = await self.iot_service.get_sensor_stats(
                sensor.id,
                start_date=datetime.now(datetime.timezone.utc) - timedelta(days=7)  # Utilisation de timezone.utc
            )
            
            health = await self.iot_service.check_sensor_health(sensor.id)
            
            sensor_data[sensor.type] = {
                "readings": readings,
                "stats": stats,
                "health": health
            }
            
        return sensor_data

    def _get_feature_name(self, index: int) -> str:
        """Retourne le nom d'une feature."""
        feature_names = [
            "Nombre_Taches",
            "Progression_Moyenne",
            "Taches_Completees",
            "Variation_Progression",
            "Taches_Bloquees",
            "Nombre_Ressources",
            "Efficacite_Moyenne",
            "Cout_Total",
            "Ressources_Humaines",
            "Ressources_Materielles",
            "Impact_Meteo",
            "Facteurs_Risque_Meteo",
            "Taches_Affectees_Meteo",
            "Risque_Precipitation",
            "Risque_Temperature"
        ]
        
        if index < len(feature_names):
            return feature_names[index]
        
        # Features IoT
        sensor_types = list(SensorType)
        sensor_index = (index - len(feature_names)) // 5
        metric_index = (index - len(feature_names)) % 5
        
        if sensor_index < len(sensor_types):
            metrics = ["Moyenne", "Minimum", "Maximum", "Statut", "Batterie"]
            return f"{sensor_types[sensor_index]}_{metrics[metric_index]}"
            
        return f"Feature_{index}"

    def _get_risk_description(self, feature_index: int, feature_value: float) -> str:
        """Génère une description du risque."""
        feature_name = self._get_feature_name(feature_index)
        
        if "Taches" in feature_name:
            if feature_value < 0.5:
                return "Progression des tâches insuffisante"
            return "Progression des tâches satisfaisante"
            
        if "Ressources" in feature_name:
            if feature_value < 0.6:
                return "Allocation des ressources sous-optimale"
            return "Allocation des ressources optimale"
            
        if "Meteo" in feature_name:
            if feature_value > 0.7:
                return "Risques météorologiques élevés"
            return "Conditions météorologiques favorables"
            
        if any(t.value in feature_name for t in SensorType):
            if feature_value < 0.4:
                return "Données capteurs hors plage optimale"
            return "Données capteurs dans la plage optimale"
            
        return "Impact modéré sur le projet"

    def _calculate_success_features(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        weather: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> np.ndarray:
        """Calcule les features pour la prédiction."""
        features = []
        
        # Features tâches
        features.extend([
            len(tasks),
            np.mean([t["progress"] for t in tasks]),
            len([t for t in tasks if t["status"] == TaskStatus.COMPLETED]),
            np.std([t["progress"] for t in tasks]),
            len([t for t in tasks if t["status"] == TaskStatus.BLOCKED])
        ])
        
        # Features ressources
        features.extend([
            len(resources),
            np.mean([r["efficiency"] for r in resources]),
            np.sum([r["cost"] for r in resources]),
            len([r for r in resources if r["type"] == ResourceType.HUMAN]),
            len([r for r in resources if r["type"] == ResourceType.MATERIAL])
        ])
        
        # Features météo
        features.extend([
            weather["impact_score"],
            len(weather["risk_factors"]),
            len(weather["affected_tasks"]),
            weather.get("precipitation_risk", 0),
            weather.get("temperature_risk", 0)
        ])
        
        # Features IoT
        for sensor_type in SensorType:
            sensor_info = iot_data.get(sensor_type, {})
            if sensor_info:
                stats = sensor_info["stats"]
                health = sensor_info["health"]
                features.extend([
                    stats["moyenne"],
                    stats["minimum"],
                    stats["maximum"],
                    1 if health["status"] == SensorStatus.ACTIF else 0,
                    health.get("battery_level", 0) / 100
                ])
            else:
                features.extend([0, 0, 0, 0, 0])
        
        return np.array(features).reshape(1, -1)

    async def _predict_success(self, features: np.ndarray) -> Dict[str, Any]:
        """Prédit le succès du projet."""
        # Normalisation
        normalized_features = self.scaler.fit_transform(features)
        
        # Prédiction
        success_proba = self.model.predict_proba(normalized_features)[0][1]
        
        # Analyse des facteurs de risque
        risk_factors = []
        feature_importance = self.model.feature_importances_
        
        for i, importance in enumerate(feature_importance):
            if importance > 0.1:
                risk_factors.append({
                    "factor": self._get_feature_name(i),
                    "impact": float(importance),
                    "description": self._get_risk_description(i, features[0][i])
                })
        
        # Génération recommandations
        recommendations = []
        for risk in risk_factors:
            if "Tâches" in risk["factor"]:
                recommendations.append({
                    "type": "TASK",
                    "priority": "HIGH" if risk["impact"] > 0.3 else "MEDIUM",
                    "description": "Optimisation des tâches requise",
                    "actions": [
                        "Revoir la planification",
                        "Identifier les blocages",
                        "Réaffecter les ressources"
                    ]
                })
            elif "Ressources" in risk["factor"]:
                recommendations.append({
                    "type": "RESOURCE",
                    "priority": "HIGH" if risk["impact"] > 0.3 else "MEDIUM",
                    "description": "Optimisation des ressources nécessaire",
                    "actions": [
                        "Évaluer les besoins",
                        "Réorganiser l'allocation",
                        "Former les équipes"
                    ]
                })
            elif "Météo" in risk["factor"]:
                recommendations.append({
                    "type": "WEATHER",
                    "priority": "HIGH" if risk["impact"] > 0.3 else "MEDIUM",
                    "description": "Adaptation aux conditions météo requise",
                    "actions": [
                        "Planifier des alternatives",
                        "Renforcer la surveillance",
                        "Préparer les protections"
                    ]
                })
            elif any(t.value in risk["factor"] for t in SensorType):
                recommendations.append({
                    "type": "IOT",
                    "priority": "HIGH" if risk["impact"] > 0.3 else "MEDIUM",
                    "description": "Optimisation du monitoring IoT nécessaire",
                    "actions": [
                        "Vérifier les capteurs",
                        "Ajuster les seuils",
                        "Améliorer la couverture"
                    ]
                })
        
        return {
            "probability": float(success_proba),
            "risk_factors": risk_factors,
            "recommendations": recommendations
        }
