"""Service de monitoring IoT pour l'agriculture de précision."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.iot_sensor import IoTSensor, SensorReading, SensorType, SensorStatus
from services.iot_service import IoTService
from services.weather_service import WeatherService
from services.ml.production.service import ProductionMLService
from core.config import settings

class IoTMonitoringService:
    """Service de monitoring des capteurs IoT."""

    def __init__(
        self,
        db: Session,
        iot_service: IoTService,
        weather_service: WeatherService,
        ml_service: ProductionMLService
    ):
        self.db = db
        self.iot_service = iot_service
        self.weather_service = weather_service
        self.ml_service = ml_service

    async def get_parcelle_monitoring(
        self,
        parcelle_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Récupère les données de monitoring pour une parcelle."""
        # Dates par défaut
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=7)

        # Récupération des capteurs
        sensors = await self.iot_service.get_sensors_by_parcelle(parcelle_id)
        
        # Données de monitoring
        monitoring_data = {
            "parcelle_id": parcelle_id,
            "periode": {
                "debut": start_date,
                "fin": end_date
            },
            "capteurs": await self._get_sensors_status(sensors),
            "mesures": await self._get_sensors_readings(sensors, start_date, end_date),
            "alertes": await self._get_sensors_alerts(sensors, start_date, end_date),
            "predictions": await self._get_ml_predictions(parcelle_id, sensors, end_date),
            "sante_systeme": await self._get_system_health(sensors)
        }

        return monitoring_data

    async def _get_sensors_status(self, sensors: List[IoTSensor]) -> List[Dict[str, Any]]:
        """Récupère l'état de tous les capteurs."""
        sensors_status = []
        for sensor in sensors:
            health = await self.iot_service.check_sensor_health(sensor.id)
            sensors_status.append({
                "id": sensor.id,
                "code": sensor.code,
                "type": sensor.type,
                "status": health["status"],
                "message": health["message"],
                "batterie": health["battery_level"],
                "signal": health["signal_quality"],
                "derniere_lecture": health["last_reading"].timestamp if health["last_reading"] else None
            })
        return sensors_status

    async def _get_sensors_readings(
        self,
        sensors: List[IoTSensor],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Récupère et agrège les lectures des capteurs."""
        readings_by_type = {}
        
        for sensor in sensors:
            if sensor.type not in readings_by_type:
                readings_by_type[sensor.type] = []
                
            # Récupération des lectures
            readings = await self.iot_service.get_sensor_readings(
                sensor.id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Calcul des statistiques
            stats = await self.iot_service.get_sensor_stats(
                sensor.id,
                start_date=start_date,
                end_date=end_date
            )
            
            readings_by_type[sensor.type].append({
                "capteur_id": sensor.id,
                "lectures": readings,
                "statistiques": stats
            })

        return readings_by_type

    async def _get_sensors_alerts(
        self,
        sensors: List[IoTSensor],
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Récupère les alertes des capteurs."""
        alerts = []
        
        for sensor in sensors:
            # Vérification des seuils
            readings = await self.iot_service.get_sensor_readings(
                sensor.id,
                start_date=start_date,
                end_date=end_date
            )
            
            for reading in readings:
                if sensor.seuils_alerte:
                    if 'min' in sensor.seuils_alerte and reading.valeur < sensor.seuils_alerte['min']:
                        alerts.append({
                            "capteur_id": sensor.id,
                            "type": "seuil_min",
                            "valeur": reading.valeur,
                            "seuil": sensor.seuils_alerte['min'],
                            "timestamp": reading.timestamp,
                            "message": f"Valeur sous le seuil minimum ({reading.valeur} < {sensor.seuils_alerte['min']})"
                        })
                    
                    if 'max' in sensor.seuils_alerte and reading.valeur > sensor.seuils_alerte['max']:
                        alerts.append({
                            "capteur_id": sensor.id,
                            "type": "seuil_max",
                            "valeur": reading.valeur,
                            "seuil": sensor.seuils_alerte['max'],
                            "timestamp": reading.timestamp,
                            "message": f"Valeur au-dessus du seuil maximum ({reading.valeur} > {sensor.seuils_alerte['max']})"
                        })

            # Vérification santé capteur
            health = await self.iot_service.check_sensor_health(sensor.id)
            if health["status"] in [SensorStatus.MAINTENANCE, SensorStatus.ERREUR]:
                alerts.append({
                    "capteur_id": sensor.id,
                    "type": "sante_capteur",
                    "status": health["status"],
                    "message": health["message"],
                    "timestamp": datetime.utcnow()
                })

        return alerts

    async def _get_ml_predictions(
        self,
        parcelle_id: UUID,
        sensors: List[IoTSensor],
        reference_date: datetime
    ) -> Dict[str, Any]:
        """Récupère les prédictions ML basées sur les données des capteurs."""
        # Récupération données météo
        weather = await self.weather_service.get_forecast(
            latitude=sensors[0].latitude,
            longitude=sensors[0].longitude,
            days=7
        )

        # Préparation données capteurs pour ML
        sensor_data = {}
        for sensor in sensors:
            readings = await self.iot_service.get_sensor_readings(
                sensor.id,
                start_date=reference_date - timedelta(days=30),
                end_date=reference_date
            )
            sensor_data[sensor.type] = readings

        # Génération prédictions
        predictions = await self.ml_service.analyze_meteo_impact(
            str(parcelle_id),
            reference_date.date(),
            (reference_date + timedelta(days=7)).date()
        )

        return predictions

    async def _get_system_health(self, sensors: List[IoTSensor]) -> Dict[str, Any]:
        """Évalue la santé globale du système IoT."""
        total_sensors = len(sensors)
        active_sensors = 0
        maintenance_needed = 0
        error_sensors = 0
        low_battery = 0
        low_signal = 0

        for sensor in sensors:
            health = await self.iot_service.check_sensor_health(sensor.id)
            
            if health["status"] == SensorStatus.ACTIF:
                active_sensors += 1
            elif health["status"] == SensorStatus.MAINTENANCE:
                maintenance_needed += 1
            elif health["status"] == SensorStatus.ERREUR:
                error_sensors += 1

            if health["battery_level"] and health["battery_level"] < 20:
                low_battery += 1
            if health["signal_quality"] and health["signal_quality"] < 30:
                low_signal += 1

        return {
            "total_capteurs": total_sensors,
            "capteurs_actifs": active_sensors,
            "capteurs_maintenance": maintenance_needed,
            "capteurs_erreur": error_sensors,
            "batterie_faible": low_battery,
            "signal_faible": low_signal,
            "sante_globale": (active_sensors / total_sensors) if total_sensors > 0 else 0,
            "timestamp": datetime.utcnow()
        }

    async def get_monitoring_dashboard(self, parcelle_id: UUID) -> Dict[str, Any]:
        """Génère les données pour le dashboard de monitoring."""
        # Périodes d'analyse
        now = datetime.utcnow()
        periods = {
            "24h": now - timedelta(days=1),
            "7j": now - timedelta(days=7),
            "30j": now - timedelta(days=30)
        }

        dashboard_data = {
            "temps_reel": await self.get_parcelle_monitoring(
                parcelle_id=parcelle_id,
                start_date=now - timedelta(hours=1),
                end_date=now
            ),
            "historique": {
                period: await self.get_parcelle_monitoring(
                    parcelle_id=parcelle_id,
                    start_date=start_date,
                    end_date=now
                )
                for period, start_date in periods.items()
            },
            "predictions": await self._get_ml_predictions(
                parcelle_id=parcelle_id,
                sensors=await self.iot_service.get_sensors_by_parcelle(parcelle_id),
                reference_date=now
            ),
            "maintenance": await self._get_maintenance_recommendations(parcelle_id)
        }

        return dashboard_data

    async def _get_maintenance_recommendations(self, parcelle_id: UUID) -> List[Dict[str, Any]]:
        """Génère des recommandations de maintenance basées sur l'état des capteurs."""
        sensors = await self.iot_service.get_sensors_by_parcelle(parcelle_id)
        recommendations = []

        for sensor in sensors:
            health = await self.iot_service.check_sensor_health(sensor.id)
            
            if health["status"] in [SensorStatus.MAINTENANCE, SensorStatus.ERREUR]:
                recommendations.append({
                    "capteur_id": sensor.id,
                    "code": sensor.code,
                    "type": sensor.type,
                    "priorite": "haute" if health["status"] == SensorStatus.ERREUR else "moyenne",
                    "raison": health["message"],
                    "action_recommandee": self._get_maintenance_action(health),
                    "deadline": datetime.utcnow() + timedelta(days=1 if health["status"] == SensorStatus.ERREUR else 7)
                })
            elif health["battery_level"] and health["battery_level"] < 20:
                recommendations.append({
                    "capteur_id": sensor.id,
                    "code": sensor.code,
                    "type": sensor.type,
                    "priorite": "moyenne",
                    "raison": f"Batterie faible ({health['battery_level']}%)",
                    "action_recommandee": "Remplacement batterie",
                    "deadline": datetime.utcnow() + timedelta(days=3)
                })
            elif health["signal_quality"] and health["signal_quality"] < 30:
                recommendations.append({
                    "capteur_id": sensor.id,
                    "code": sensor.code,
                    "type": sensor.type,
                    "priorite": "basse",
                    "raison": f"Signal faible ({health['signal_quality']}%)",
                    "action_recommandee": "Vérification position/obstacles",
                    "deadline": datetime.utcnow() + timedelta(days=5)
                })

        return recommendations

    def _get_maintenance_action(self, health: Dict[str, Any]) -> str:
        """Détermine l'action de maintenance recommandée."""
        if not health["last_reading"]:
            return "Vérification connexion capteur"
        if health["battery_level"] and health["battery_level"] < 10:
            return "Remplacement urgent batterie"
        if health["signal_quality"] and health["signal_quality"] < 20:
            return "Repositionnement capteur"
        return "Inspection et diagnostic"
