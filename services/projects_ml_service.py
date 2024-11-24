"""
Service d'apprentissage automatique pour les projets agricoles
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from models.production import Parcelle, CultureType
from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService

class ProjectsMLService:
    """Service ML pour l'optimisation des projets agricoles"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db)
        self.cache = CacheService()

    async def predict_project_success(
        self,
        project_id: str,
        current_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Prédit la probabilité de succès d'un projet"""
        # Récupération des données
        tasks = await self._get_project_tasks(project_id)
        resources = await self._get_project_resources(project_id)
        weather = await self._get_weather_impact(project_id)
        
        # Calcul des features
        features = self._calculate_success_features(tasks, resources, weather)
        
        # Prédiction
        prediction = await self._predict_success(features)
        
        return {
            "success_probability": float(prediction["probability"]),
            "risk_factors": prediction["risk_factors"],
            "recommendations": await self._generate_recommendations(
                project_id,
                prediction
            )
        }

    async def optimize_resource_allocation(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Optimise l'allocation des ressources du projet"""
        # Récupération données
        tasks = await self._get_project_tasks(project_id)
        resources = await self._get_available_resources(start_date, end_date)
        constraints = await self._get_resource_constraints(project_id)
        
        # Optimisation
        allocation = await self._optimize_allocation(
            tasks,
            resources,
            constraints
        )
        
        return {
            "optimal_allocation": allocation["allocation"],
            "efficiency_score": allocation["efficiency"],
            "bottlenecks": allocation["bottlenecks"],
            "recommendations": allocation["recommendations"]
        }

    async def analyze_project_performance(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse détaillée de la performance du projet"""
        # Récupération données
        tasks = await self._get_project_tasks(project_id)
        resources = await self._get_project_resources(project_id)
        timeline = await self._get_project_timeline(project_id)
        
        # Analyse KPIs
        kpis = self._calculate_project_kpis(tasks, resources, timeline)
        
        # Analyse tendances
        trends = self._analyze_performance_trends(tasks, timeline)
        
        # Prédictions
        predictions = await self._predict_future_performance(
            project_id,
            kpis,
            trends
        )
        
        return {
            "kpis": kpis,
            "trends": trends,
            "predictions": predictions,
            "recommendations": await self._generate_performance_recommendations(
                project_id,
                kpis,
                trends
            )
        }

    async def predict_weather_impact(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Prédit l'impact de la météo sur le projet"""
        # Récupération données
        weather = await self.weather_service.get_forecast(
            start_date,
            end_date
        )
        tasks = await self._get_weather_sensitive_tasks(project_id)
        
        # Analyse impact
        impact = self._analyze_weather_impact(weather, tasks)
        
        # Génération alternatives
        alternatives = await self._generate_weather_alternatives(
            project_id,
            impact
        )
        
        return {
            "impact_score": impact["score"],
            "affected_tasks": impact["tasks"],
            "risk_periods": impact["risks"],
            "alternatives": alternatives
        }

    async def _get_project_tasks(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère les tâches d'un projet avec leurs métriques"""
        tasks = self.db.query(Task).filter(
            Task.project_id == project_id
        ).all()
        
        return [{
            "id": t.id,
            "name": t.name,
            "status": t.status,
            "start_date": t.start_date,
            "end_date": t.end_date,
            "progress": t.progress,
            "dependencies": t.dependencies,
            "resources": t.resources,
            "metrics": t.metrics
        } for t in tasks]

    async def _get_project_resources(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère les ressources allouées à un projet"""
        resources = self.db.query(Resource).filter(
            Resource.project_id == project_id
        ).all()
        
        return [{
            "id": r.id,
            "type": r.type,
            "name": r.name,
            "availability": r.availability,
            "efficiency": r.efficiency,
            "cost": r.cost
        } for r in resources]

    async def _get_weather_impact(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """Analyse l'impact météo sur un projet"""
        # TODO: Implémenter l'analyse météo
        return {
            "impact_score": 0.7,
            "risk_factors": ["Température", "Précipitations"],
            "affected_tasks": ["Semis", "Récolte"]
        }

    def _calculate_success_features(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        weather: Dict[str, Any]
    ) -> np.ndarray:
        """Calcule les features pour la prédiction de succès"""
        features = []
        
        # Features tâches
        if tasks:
            features.extend([
                len(tasks),
                np.mean([t["progress"] for t in tasks]),
                len([t for t in tasks if t["status"] == TaskStatus.COMPLETED])
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features ressources
        if resources:
            features.extend([
                len(resources),
                np.mean([r["efficiency"] for r in resources]),
                np.sum([r["cost"] for r in resources])
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features météo
        features.extend([
            weather["impact_score"],
            len(weather["risk_factors"]),
            len(weather["affected_tasks"])
        ])
            
        return np.array(features)

    async def _predict_success(
        self,
        features: np.ndarray
    ) -> Dict[str, Any]:
        """Prédit le succès du projet"""
        # TODO: Implémenter le modèle ML
        # Pour l'instant, utilise une moyenne pondérée
        weights = np.array([0.1, 0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.05, 0.05])
        probability = float(np.sum(features * weights))
        
        return {
            "probability": probability,
            "risk_factors": [
                {
                    "factor": "Ressources",
                    "impact": 0.3,
                    "description": "Allocation sous-optimale"
                },
                {
                    "factor": "Météo",
                    "impact": 0.2,
                    "description": "Risques climatiques"
                }
            ]
        }

    async def _generate_recommendations(
        self,
        project_id: str,
        prediction: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur la prédiction"""
        recommendations = []
        
        # Recommandations ressources
        if any(rf["factor"] == "Ressources" for rf in prediction["risk_factors"]):
            recommendations.append({
                "type": "RESOURCE",
                "priority": "HIGH",
                "description": "Optimiser l'allocation des ressources",
                "actions": [
                    "Revoir la planification des ressources",
                    "Identifier les goulots d'étranglement"
                ]
            })
            
        # Recommandations météo
        if any(rf["factor"] == "Météo" for rf in prediction["risk_factors"]):
            recommendations.append({
                "type": "WEATHER",
                "priority": "MEDIUM",
                "description": "Anticiper les risques météo",
                "actions": [
                    "Planifier des alternatives",
                    "Renforcer le monitoring"
                ]
            })
            
        return recommendations

    async def _optimize_allocation(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimise l'allocation des ressources"""
        # TODO: Implémenter l'algorithme d'optimisation
        return {
            "allocation": [
                {
                    "task_id": "T1",
                    "resources": ["R1", "R2"],
                    "start_date": date.today(),
                    "end_date": date.today() + timedelta(days=7)
                }
            ],
            "efficiency": 0.85,
            "bottlenecks": [
                {
                    "resource": "R1",
                    "period": "2024-02",
                    "utilization": 0.95
                }
            ],
            "recommendations": [
                "Répartir la charge de R1",
                "Ajouter des ressources en février"
            ]
        }

    def _calculate_project_kpis(
        self,
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        timeline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calcule les KPIs du projet"""
        return {
            "schedule_performance": 0.85,
            "cost_performance": 0.92,
            "resource_efficiency": 0.78,
            "quality_score": 0.88,
            "risk_score": 0.25
        }

    def _analyze_performance_trends(
        self,
        tasks: List[Dict[str, Any]],
        timeline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse les tendances de performance"""
        return {
            "velocity": {
                "current": 8.5,
                "trend": "increasing",
                "forecast": 9.2
            },
            "completion_rate": {
                "current": 0.82,
                "trend": "stable",
                "forecast": 0.85
            },
            "resource_usage": {
                "current": 0.75,
                "trend": "decreasing",
                "forecast": 0.70
            }
        }

    async def _predict_future_performance(
        self,
        project_id: str,
        kpis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prédit la performance future du projet"""
        return {
            "completion_date": date.today() + timedelta(days=30),
            "final_cost": 150000,
            "quality_forecast": 0.90,
            "risk_forecast": 0.20
        }

    async def _generate_performance_recommendations(
        self,
        project_id: str,
        kpis: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur la performance"""
        recommendations = []
        
        # Recommandations planning
        if kpis["schedule_performance"] < 0.9:
            recommendations.append({
                "type": "SCHEDULE",
                "priority": "HIGH",
                "description": "Améliorer la performance planning",
                "actions": [
                    "Identifier les retards",
                    "Optimiser les dépendances"
                ]
            })
            
        # Recommandations coûts
        if kpis["cost_performance"] < 0.9:
            recommendations.append({
                "type": "COST",
                "priority": "MEDIUM",
                "description": "Optimiser les coûts",
                "actions": [
                    "Revoir l'allocation budget",
                    "Identifier sources surcoût"
                ]
            })
            
        return recommendations

    async def _get_weather_sensitive_tasks(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Identifie les tâches sensibles à la météo"""
        tasks = self.db.query(Task).filter(
            and_(
                Task.project_id == project_id,
                Task.weather_sensitive == True
            )
        ).all()
        
        return [{
            "id": t.id,
            "name": t.name,
            "weather_conditions": t.weather_conditions,
            "flexibility": t.flexibility
        } for t in tasks]

    def _analyze_weather_impact(
        self,
        weather: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyse l'impact de la météo sur les tâches"""
        return {
            "score": 0.65,
            "tasks": [
                {
                    "task_id": "T1",
                    "impact": "HIGH",
                    "conditions": ["RAIN", "WIND"]
                }
            ],
            "risks": [
                {
                    "period": "2024-02",
                    "risk": "HIGH",
                    "conditions": ["FROST"]
                }
            ]
        }

    async def _generate_weather_alternatives(
        self,
        project_id: str,
        impact: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des alternatives pour les périodes à risque"""
        return [
            {
                "task_id": "T1",
                "original_date": date(2024, 2, 1),
                "alternative_date": date(2024, 2, 15),
                "reason": "Éviter période gel"
            }
        ]
