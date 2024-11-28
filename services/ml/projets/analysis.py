"""Service d'analyse de performance des projets."""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import numpy as np
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.resource import Resource
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.iot_service import IoTService
from services.cache_service import CacheService

class PerformanceAnalyzer:
    """Analyseur de performance des projets."""
    
    def __init__(self, db: Session):
        """Initialisation de l'analyseur."""
        self.db = db
        self.iot_service = IoTService(db)
        self.cache = CacheService()

    async def analyze_performance(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse détaillée de la performance du projet."""
        # Vérification du cache
        cache_key = f"performance_{project_id}_{start_date}_{end_date}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Récupération données
        tasks = await self._get_tasks(project_id)
        resources = await self._get_resources(project_id)
        iot_data = await self._get_iot_data(project_id)
        
        # Calcul KPIs
        kpis = {
            "schedule_performance": self._calculate_schedule_performance(tasks),
            "cost_performance": self._calculate_cost_performance(tasks, resources),
            "resource_efficiency": self._calculate_resource_efficiency(tasks, resources),
            "quality_score": self._calculate_quality_score(tasks, iot_data),
            "risk_score": self._calculate_risk_score(tasks, iot_data)
        }
        
        # Analyse tendances
        trends = {
            "velocity": self._analyze_velocity_trend(tasks),
            "completion_rate": self._analyze_completion_trend(tasks),
            "resource_usage": self._analyze_resource_trend(tasks, resources),
            "quality_trend": self._analyze_quality_trend(tasks, iot_data),
            "risk_trend": self._analyze_risk_trend(tasks, iot_data)
        }
        
        # Prédictions
        predictions = {
            "completion_date": self._predict_completion_date(tasks, trends),
            "final_cost": self._predict_final_cost(tasks, resources, trends),
            "quality_forecast": self._predict_quality(tasks, iot_data, trends),
            "risk_forecast": self._predict_risk(tasks, iot_data, trends)
        }
        
        # Recommandations
        recommendations = self._generate_recommendations(kpis, trends, predictions)
        
        result = {
            "kpis": kpis,
            "trends": trends,
            "predictions": predictions,
            "recommendations": recommendations
        }
        
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def _get_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les tâches du projet."""
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        return [{
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "progress": task.progress,
            "metrics": task.metrics
        } for task in tasks]

    async def _get_resources(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les ressources du projet."""
        resources = self.db.query(Resource).filter(
            Resource.project_id == project_id
        ).all()
        return [{
            "id": resource.id,
            "type": resource.type,
            "efficiency": resource.efficiency,
            "cost": float(resource.cost)
        } for resource in resources]

    async def _get_iot_data(self, project_id: str) -> Dict[str, Any]:
        """Récupère les données IoT du projet."""
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

    def _calculate_schedule_performance(self, tasks: List[Dict[str, Any]]) -> float:
        """Calcule la performance planning."""
        if not tasks:
            return 0.0
            
        completed = len([t for t in tasks if t["status"] == TaskStatus.COMPLETED])
        total = len(tasks)
        
        planned_progress = sum(
            (datetime.now().date() - t["start_date"]).days /
            ((t["end_date"] - t["start_date"]).days + 1)
            for t in tasks
        ) / total
        
        actual_progress = sum(t["progress"] for t in tasks) / (total * 100)
        
        return min(actual_progress / planned_progress if planned_progress > 0 else 0, 1)

    def _calculate_cost_performance(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]]
    ) -> float:
        """Calcule la performance coût."""
        if not tasks or not resources:
            return 0.0
            
        planned_cost = sum(r["cost"] for r in resources)
        actual_cost = sum(
            r["cost"] * (t["progress"] / 100)
            for t in tasks
            for r in t.get("resources", [])
        )
        
        return min(planned_cost / actual_cost if actual_cost > 0 else 0, 1)

    def _calculate_resource_efficiency(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]]
    ) -> float:
        """Calcule l'efficacité des ressources."""
        if not tasks or not resources:
            return 0.0
            
        total_efficiency = sum(r["efficiency"] for r in resources)
        actual_efficiency = sum(
            r["efficiency"] * (t["progress"] / 100)
            for t in tasks
            for r in t.get("resources", [])
        )
        
        return actual_efficiency / total_efficiency if total_efficiency > 0 else 0

    def _calculate_quality_score(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any]
    ) -> float:
        """Calcule le score qualité."""
        if not tasks or not iot_data:
            return 0.0
            
        # Score basé sur les métriques des tâches
        task_quality = np.mean([
            t.get("metrics", {}).get("quality", 0.8)
            for t in tasks
        ])
        
        # Score basé sur les données IoT
        iot_quality = np.mean([
            1.0 if s["health"]["status"] == SensorStatus.ACTIF else 0.5
            for s in iot_data.values()
        ])
        
        return (task_quality + iot_quality) / 2

    def _calculate_risk_score(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any]
    ) -> float:
        """Calcule le score de risque."""
        if not tasks:
            return 0.0
            
        # Risques liés aux tâches
        task_risks = [
            1.0 if t["status"] == TaskStatus.BLOCKED else
            0.7 if t["status"] == TaskStatus.AT_RISK else
            0.3 if t["progress"] < 50 else
            0.1
            for t in tasks
        ]
        
        # Risques liés aux capteurs
        iot_risks = [
            0.8 if s["health"]["status"] != SensorStatus.ACTIF else
            0.5 if s["health"].get("battery_level", 100) < 30 else
            0.2
            for s in iot_data.values()
        ] if iot_data else [0.0]
        
        return np.mean(task_risks + iot_risks)

    def _analyze_velocity_trend(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse la tendance de vélocité."""
        if not tasks:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        # Calcul vélocité actuelle
        completed_tasks = [
            t for t in tasks
            if t["status"] == TaskStatus.COMPLETED
        ]
        
        if not completed_tasks:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        current_velocity = len(completed_tasks) / max(
            (datetime.now().date() - min(t["start_date"] for t in tasks)).days,
            1
        )
        
        # Analyse tendance
        velocities = []
        for week in range(4):
            week_start = datetime.now().date() - timedelta(weeks=week+1)
            week_end = datetime.now().date() - timedelta(weeks=week)
            
            week_completed = len([
                t for t in completed_tasks
                if week_start <= t["end_date"] <= week_end
            ])
            
            velocities.append(week_completed / 7)
        
        trend = "increasing" if np.mean(velocities[:2]) > np.mean(velocities[2:]) else \
               "decreasing" if np.mean(velocities[:2]) < np.mean(velocities[2:]) else \
               "stable"
        
        # Prévision
        forecast = current_velocity * (
            1.1 if trend == "increasing" else
            0.9 if trend == "decreasing" else
            1.0
        )
        
        return {
            "current": current_velocity,
            "trend": trend,
            "forecast": forecast
        }

    def _analyze_completion_trend(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyse la tendance de complétion."""
        if not tasks:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        current_rate = len([
            t for t in tasks
            if t["status"] == TaskStatus.COMPLETED
        ]) / len(tasks)
        
        # Analyse tendance sur 4 semaines
        completion_rates = []
        for week in range(4):
            week_end = datetime.now().date() - timedelta(weeks=week)
            completed_at_week = len([
                t for t in tasks
                if t["status"] == TaskStatus.COMPLETED and t["end_date"] <= week_end
            ])
            completion_rates.append(completed_at_week / len(tasks))
        
        trend = "increasing" if np.mean(completion_rates[:2]) > np.mean(completion_rates[2:]) else \
               "decreasing" if np.mean(completion_rates[:2]) < np.mean(completion_rates[2:]) else \
               "stable"
        
        # Prévision
        forecast = min(
            current_rate * (
                1.1 if trend == "increasing" else
                0.9 if trend == "decreasing" else
                1.0
            ),
            1.0
        )
        
        return {
            "current": current_rate,
            "trend": trend,
            "forecast": forecast
        }

    def _analyze_resource_trend(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyse la tendance d'utilisation des ressources."""
        if not tasks or not resources:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        # Calcul utilisation actuelle
        current_usage = sum(
            len(t.get("resources", [])) / len(resources)
            for t in tasks
            if t["status"] in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]
        ) / len(tasks)
        
        # Analyse tendance sur 4 semaines
        usage_rates = []
        for week in range(4):
            week_end = datetime.now().date() - timedelta(weeks=week)
            active_tasks = [
                t for t in tasks
                if t["status"] in [TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]
                and t["start_date"] <= week_end
            ]
            if active_tasks:
                usage = sum(
                    len(t.get("resources", [])) / len(resources)
                    for t in active_tasks
                ) / len(active_tasks)
                usage_rates.append(usage)
            else:
                usage_rates.append(0.0)
        
        trend = "increasing" if np.mean(usage_rates[:2]) > np.mean(usage_rates[2:]) else \
               "decreasing" if np.mean(usage_rates[:2]) < np.mean(usage_rates[2:]) else \
               "stable"
        
        # Prévision
        forecast = min(
            current_usage * (
                1.1 if trend == "increasing" else
                0.9 if trend == "decreasing" else
                1.0
            ),
            1.0
        )
        
        return {
            "current": current_usage,
            "trend": trend,
            "forecast": forecast
        }

    def _analyze_quality_trend(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse la tendance de qualité."""
        if not tasks or not iot_data:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        # Calcul qualité actuelle
        current_quality = self._calculate_quality_score(tasks, iot_data)
        
        # Analyse tendance sur 4 semaines
        quality_scores = []
        for week in range(4):
            week_end = datetime.now().date() - timedelta(weeks=week)
            tasks_at_week = [
                t for t in tasks
                if t["start_date"] <= week_end
            ]
            if tasks_at_week:
                score = self._calculate_quality_score(tasks_at_week, iot_data)
                quality_scores.append(score)
            else:
                quality_scores.append(0.0)
        
        trend = "increasing" if np.mean(quality_scores[:2]) > np.mean(quality_scores[2:]) else \
               "decreasing" if np.mean(quality_scores[:2]) < np.mean(quality_scores[2:]) else \
               "stable"
        
        # Prévision
        forecast = min(
            current_quality * (
                1.1 if trend == "increasing" else
                0.9 if trend == "decreasing" else
                1.0
            ),
            1.0
        )
        
        return {
            "current": current_quality,
            "trend": trend,
            "forecast": forecast
        }

    def _analyze_risk_trend(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse la tendance de risque."""
        if not tasks:
            return {
                "current": 0.0,
                "trend": "stable",
                "forecast": 0.0
            }
            
        # Calcul risque actuel
        current_risk = self._calculate_risk_score(tasks, iot_data)
        
        # Analyse tendance sur 4 semaines
        risk_scores = []
        for week in range(4):
            week_end = datetime.now().date() - timedelta(weeks=week)
            tasks_at_week = [
                t for t in tasks
                if t["start_date"] <= week_end
            ]
            if tasks_at_week:
                score = self._calculate_risk_score(tasks_at_week, iot_data)
                risk_scores.append(score)
            else:
                risk_scores.append(0.0)
        
        trend = "increasing" if np.mean(risk_scores[:2]) > np.mean(risk_scores[2:]) else \
               "decreasing" if np.mean(risk_scores[:2]) < np.mean(risk_scores[2:]) else \
               "stable"
        
        # Prévision
        forecast = min(
            current_risk * (
                1.1 if trend == "increasing" else
                0.9 if trend == "decreasing" else
                1.0
            ),
            1.0
        )
        
        return {
            "current": current_risk,
            "trend": trend,
            "forecast": forecast
        }

    def _predict_completion_date(
        self,
        tasks: List[Dict[str, Any]],
        trends: Dict[str, Any]
    ) -> date:
        """Prédit la date de fin du projet."""
        if not tasks:
            return datetime.now().date()
            
        remaining_tasks = len([
            t for t in tasks
            if t["status"] != TaskStatus.COMPLETED
        ])
        
        if remaining_tasks == 0:
            return max(t["end_date"] for t in tasks)
            
        velocity = trends["velocity"]["forecast"]
        if velocity <= 0:
            velocity = 0.1  # Valeur minimale pour éviter division par zéro
            
        days_remaining = remaining_tasks / velocity
        
        return datetime.now().date() + timedelta(days=int(days_remaining))

    def _predict_final_cost(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        trends: Dict[str, Any]
    ) -> float:
        """Prédit le coût final du projet."""
        if not tasks or not resources:
            return 0.0
            
        current_cost = sum(
            r["cost"] * (t["progress"] / 100)
            for t in tasks
            for r in t.get("resources", [])
        )
        
        remaining_work = 1 - trends["completion_rate"]["current"]
        cost_efficiency = trends["resource_usage"]["forecast"]
        
        return current_cost * (1 + remaining_work * cost_efficiency)

    def _predict_quality(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> float:
        """Prédit la qualité finale du projet."""
        if not tasks or not iot_data:
            return 0.0
            
        current_quality = self._calculate_quality_score(tasks, iot_data)
        quality_trend = trends["quality_trend"]["forecast"]
        
        return min(current_quality * quality_trend, 1.0)

    def _predict_risk(
        self,
        tasks: List[Dict[str, Any]],
        iot_data: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> float:
        """Prédit le risque final du projet."""
        if not tasks:
            return 0.0
            
        current_risk = self._calculate_risk_score(tasks, iot_data)
        risk_trend = trends["risk_trend"]["forecast"]
        
        return min(current_risk * risk_trend, 1.0)

    def _generate_recommendations(
        self,
        kpis: Dict[str, float],
        trends: Dict[str, Any],
        predictions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur l'analyse."""
        recommendations = []
        
        # Recommandations planning
        if kpis["schedule_performance"] < 0.8:
            recommendations.append({
                "type": "SCHEDULE",
                "priority": "HIGH",
                "description": "Retard dans le planning",
                "actions": [
                    "Identifier les tâches critiques",
                    "Réaffecter les ressources",
                    "Ajuster les dépendances"
                ]
            })
        
        # Recommandations coûts
        if kpis["cost_performance"] < 0.85:
            recommendations.append({
                "type": "COST",
                "priority": "HIGH",
                "description": "Dépassement budgétaire",
                "actions": [
                    "Optimiser l'utilisation des ressources",
                    "Revoir les estimations",
                    "Identifier les sources de surcoût"
                ]
            })
        
        # Recommandations qualité
        if kpis["quality_score"] < 0.9:
            recommendations.append({
                "type": "QUALITY",
                "priority": "MEDIUM",
                "description": "Qualité sous-optimale",
                "actions": [
                    "Renforcer les contrôles",
                    "Former les équipes",
                    "Améliorer les processus"
                ]
            })
        
        # Recommandations risques
        if kpis["risk_score"] > 0.7:
            recommendations.append({
                "type": "RISK",
                "priority": "HIGH",
                "description": "Niveau de risque élevé",
                "actions": [
                    "Mettre en place des actions préventives",
                    "Renforcer le suivi",
                    "Préparer des plans de contingence"
                ]
            })
        
        # Recommandations tendances
        if trends["velocity"]["trend"] == "decreasing":
            recommendations.append({
                "type": "VELOCITY",
                "priority": "MEDIUM",
                "description": "Baisse de la vélocité",
                "actions": [
                    "Analyser les causes du ralentissement",
                    "Optimiser les processus",
                    "Renforcer l'équipe"
                ]
            })
        
        if trends["resource_usage"]["trend"] == "increasing" and \
           trends["resource_usage"]["forecast"] > 0.9:
            recommendations.append({
                "type": "RESOURCE",
                "priority": "HIGH",
                "description": "Saturation des ressources à venir",
                "actions": [
                    "Planifier des ressources supplémentaires",
                    "Optimiser l'allocation",
                    "Revoir la planification"
                ]
            })
        
        return recommendations
