"""Service d'analyse météo des projets."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import numpy as np
from sqlalchemy.orm import Session

from models.tache import Tache, StatutTache
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService

class WeatherAnalyzer:
    """Analyseur météo pour les projets."""
    
    def __init__(self, db: Session):
        """Initialisation de l'analyseur."""
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        self.cache = CacheService()

    async def analyze_weather_impact(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Analyse l'impact météo sur le projet."""
        # Vérification du cache
        cache_key = f"weather_impact_{project_id}_{start_date}_{end_date}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Récupération données
        tasks = await self._get_weather_sensitive_tasks(project_id)
        weather = await self.weather_service.get_forecast(start_date, end_date)
        iot_data = await self._get_iot_data(project_id)
        
        # Analyse impact
        impact_score = 0.0
        affected_tasks = []
        risk_periods = []
        
        for task in tasks:
            task_weather = [
                w for w in weather["daily"]
                if start_date <= w["date"] <= end_date
            ]
            
            # Analyse conditions météo
            for condition in task_weather:
                risk_level = self._evaluate_weather_risk(
                    condition,
                    task["weather_conditions"],
                    iot_data
                )
                
                if risk_level > 0.5:
                    affected_tasks.append({
                        "task_id": task["id"],
                        "impact": "HIGH" if risk_level > 0.8 else "MEDIUM",
                        "conditions": self._get_risk_conditions(condition)
                    })
                    
                    risk_periods.append({
                        "period": condition["date"].strftime("%Y-%m"),
                        "risk": "HIGH" if risk_level > 0.8 else "MEDIUM",
                        "conditions": self._get_risk_conditions(condition)
                    })
                    
                    impact_score = max(impact_score, risk_level)
        
        # Génération alternatives
        alternatives = await self._generate_alternatives(
            tasks,
            weather,
            iot_data,
            affected_tasks,
            start_date,
            end_date
        )
        
        result = {
            "impact_score": impact_score,
            "affected_tasks": affected_tasks,
            "risk_periods": risk_periods,
            "alternatives": alternatives
        }
        
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def _get_weather_sensitive_tasks(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère les tâches sensibles à la météo."""
        tasks = self.db.query(Tache).filter(
            Tache.project_id == project_id,
            Tache.weather_sensitive == True
        ).all()
        
        return [{
            "id": task.id,
            "name": task.name,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "weather_conditions": task.weather_conditions,
            "flexibility": task.flexibility
        } for task in tasks]

    async def _get_iot_data(self, project_id: str) -> Dict[str, Any]:
        """Récupère les données IoT pertinentes."""
        sensors = await self.iot_service.get_sensors_by_parcelle(project_id)
        
        sensor_data = {}
        for sensor in sensors:
            readings = await self.iot_service.get_sensor_readings(
                sensor.id,
                start_date=datetime.utcnow() - timedelta(days=7)
            )
            
            stats = await self.iot_service.get_sensor_stats(
                sensor.id,
                start_date=datetime.utcnow() - timedelta(days=7)
            )
            
            health = await self.iot_service.check_sensor_health(sensor.id)
            
            sensor_data[sensor.type] = {
                "readings": readings,
                "stats": stats,
                "health": health
            }
            
        return sensor_data

    def _evaluate_weather_risk(
        self,
        condition: Dict[str, Any],
        task_conditions: List[str],
        iot_data: Dict[str, Any]
    ) -> float:
        """Évalue le niveau de risque météo."""
        risk_level = 0.0
        
        # Analyse température
        if "TEMPERATURE" in task_conditions:
            temp_risk = self._evaluate_temperature_risk(condition, iot_data)
            risk_level = max(risk_level, temp_risk)
        
        # Analyse précipitations
        if "RAIN" in task_conditions:
            rain_risk = self._evaluate_rain_risk(condition, iot_data)
            risk_level = max(risk_level, rain_risk)
        
        # Analyse vent
        if "WIND" in task_conditions:
            wind_risk = self._evaluate_wind_risk(condition, iot_data)
            risk_level = max(risk_level, wind_risk)
        
        # Analyse gel
        if "FROST" in task_conditions:
            frost_risk = self._evaluate_frost_risk(condition, iot_data)
            risk_level = max(risk_level, frost_risk)
        
        return risk_level

    def _evaluate_temperature_risk(
        self,
        condition: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> float:
        """Évalue le risque lié à la température."""
        # Données prévision
        forecast_temp = condition["temperature"]
        
        # Données capteurs
        if SensorType.TEMPERATURE_SOL in iot_data:
            sensor_data = iot_data[SensorType.TEMPERATURE_SOL]
            current_temp = sensor_data["stats"]["moyenne"]
            
            # Écart entre prévision et réalité
            temp_gap = abs(forecast_temp - current_temp)
            if temp_gap > 5:  # Écart significatif
                return 0.8
            elif temp_gap > 2:  # Écart modéré
                return 0.5
        
        # Seuils critiques
        if forecast_temp > 35 or forecast_temp < 5:
            return 0.9
        elif forecast_temp > 30 or forecast_temp < 10:
            return 0.6
        
        return 0.2

    def _evaluate_rain_risk(
        self,
        condition: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> float:
        """Évalue le risque lié aux précipitations."""
        # Données prévision
        forecast_rain = condition["precipitation"]
        
        # Données capteurs
        if SensorType.HUMIDITE_SOL in iot_data:
            sensor_data = iot_data[SensorType.HUMIDITE_SOL]
            current_humidity = sensor_data["stats"]["moyenne"]
            
            # Sol déjà saturé
            if current_humidity > 80:
                return 0.9
            elif current_humidity > 60:
                return 0.6
        
        # Seuils précipitations
        if forecast_rain > 20:  # Fortes pluies
            return 0.9
        elif forecast_rain > 10:  # Pluies modérées
            return 0.6
        elif forecast_rain > 5:  # Pluies légères
            return 0.3
        
        return 0.1

    def _evaluate_wind_risk(
        self,
        condition: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> float:
        """Évalue le risque lié au vent."""
        # Données prévision
        wind_speed = condition["wind_speed"]
        
        # Seuils vent
        if wind_speed > 50:  # Vent violent
            return 0.9
        elif wind_speed > 30:  # Vent fort
            return 0.7
        elif wind_speed > 20:  # Vent modéré
            return 0.4
        
        return 0.1

    def _evaluate_frost_risk(
        self,
        condition: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> float:
        """Évalue le risque lié au gel."""
        # Données prévision
        min_temp = condition["temperature_min"]
        
        # Données capteurs
        if SensorType.TEMPERATURE_SOL in iot_data:
            sensor_data = iot_data[SensorType.TEMPERATURE_SOL]
            current_temp = sensor_data["stats"]["minimum"]
            
            # Température déjà proche du gel
            if current_temp < 2:
                return 0.9
            elif current_temp < 5:
                return 0.6
        
        # Seuils gel
        if min_temp < 0:  # Gel
            return 0.9
        elif min_temp < 2:  # Risque gel
            return 0.7
        elif min_temp < 5:  # Proche gel
            return 0.4
        
        return 0.1

    def _get_risk_conditions(self, condition: Dict[str, Any]) -> List[str]:
        """Identifie les conditions à risque."""
        risks = []
        
        if condition["temperature"] > 30 or condition["temperature"] < 10:
            risks.append("TEMPERATURE")
            
        if condition["precipitation"] > 10:
            risks.append("RAIN")
            
        if condition["wind_speed"] > 30:
            risks.append("WIND")
            
        if condition["temperature_min"] < 2:
            risks.append("FROST")
            
        return risks

    async def _generate_alternatives(
        self,
        tasks: List[Dict[str, Any]],
        weather: Dict[str, Any],
        iot_data: Dict[str, Any],
        affected_tasks: List[Dict[str, Any]],
        start_date: date,
        end_date: date
    ) -> List[Dict[str, Any]]:
        """Génère des alternatives pour les tâches affectées."""
        alternatives = []
        
        for task_impact in affected_tasks:
            task = next(
                t for t in tasks
                if t["id"] == task_impact["task_id"]
            )
            
            # Recherche périodes favorables
            alt_dates = []
            current_date = start_date
            while current_date <= end_date:
                # Conditions du jour
                day_weather = next(
                    w for w in weather["daily"]
                    if w["date"] == current_date
                )
                
                # Évaluation risque
                risk = self._evaluate_weather_risk(
                    day_weather,
                    task["weather_conditions"],
                    iot_data
                )
                
                # Période favorable
                if risk < 0.3:
                    alt_dates.append(current_date)
                
                current_date += timedelta(days=1)
            
            # Génération alternative
            if alt_dates:
                alternatives.append({
                    "task_id": task["id"],
                    "original_date": task["start_date"],
                    "alternative_date": alt_dates[0],
                    "reason": f"Éviter {', '.join(task_impact['conditions'])}"
                })
        
        return alternatives
