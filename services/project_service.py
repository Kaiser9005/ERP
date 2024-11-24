"""
Service de gestion des projets avec analytics avancés
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from services.projects_ml_service import ProjectsMLService
from services.weather_service import WeatherService
from services.cache_service import CacheService

class ProjectService:
    """Service unifié pour la gestion des projets"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ml_service = ProjectsMLService(db)
        self.weather_service = WeatherService(db)
        self.cache = CacheService()

    async def get_project_details(
        self,
        project_id: str,
        include_analytics: bool = False
    ) -> Dict[str, Any]:
        """Récupère les détails d'un projet avec analytics optionnels"""
        # Détails de base
        details = await self._get_basic_details(project_id)
        
        if include_analytics:
            # Prédictions ML
            success_prediction = await self.ml_service.predict_project_success(
                project_id,
                date.today()
            )
            
            # Performance analytics
            performance = await self.ml_service.analyze_project_performance(
                project_id,
                details["start_date"],
                details["end_date"]
            )
            
            # Impact météo
            weather_impact = await self.ml_service.predict_weather_impact(
                project_id,
                details["start_date"],
                details["end_date"]
            )
            
            details.update({
                "success_prediction": success_prediction,
                "performance_analytics": performance,
                "weather_impact": weather_impact
            })
            
        return details

    async def create_project(
        self,
        project_data: Dict[str, Any],
        optimize_resources: bool = True
    ) -> Dict[str, Any]:
        """Crée un nouveau projet avec optimisation optionnelle"""
        # Création projet
        project = await self._create_basic_project(project_data)
        
        if optimize_resources:
            # Optimisation ressources
            allocation = await self.ml_service.optimize_resource_allocation(
                project.id,
                project_data["start_date"],
                project_data["end_date"]
            )
            
            # Application optimisation
            await self._apply_resource_allocation(project.id, allocation)
            
            project_data["resource_optimization"] = allocation
            
        return project_data

    async def update_project(
        self,
        project_id: str,
        project_data: Dict[str, Any],
        reoptimize: bool = True
    ) -> Dict[str, Any]:
        """Met à jour un projet avec ré-optimisation optionnelle"""
        # Mise à jour basique
        project = await self._update_basic_project(project_id, project_data)
        
        if reoptimize:
            # Ré-optimisation ressources
            allocation = await self.ml_service.optimize_resource_allocation(
                project_id,
                project.start_date,
                project.end_date
            )
            
            # Application optimisation
            await self._apply_resource_allocation(project_id, allocation)
            
            project_data["resource_optimization"] = allocation
            
        return project_data

    async def get_project_analytics(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Récupère les analytics complets d'un projet"""
        # Performance
        performance = await self.ml_service.analyze_project_performance(
            project_id,
            start_date,
            end_date
        )
        
        # Prédictions
        success_prediction = await self.ml_service.predict_project_success(
            project_id,
            date.today()
        )
        
        # Impact météo
        weather_impact = await self.ml_service.predict_weather_impact(
            project_id,
            start_date or date.today(),
            end_date or (date.today() + timedelta(days=90))
        )
        
        return {
            "performance": performance,
            "success_prediction": success_prediction,
            "weather_impact": weather_impact,
            "recommendations": await self._generate_global_recommendations(
                project_id,
                performance,
                success_prediction,
                weather_impact
            )
        }

    async def optimize_project_resources(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Optimise l'allocation des ressources d'un projet"""
        # Récupération dates
        project = await self._get_basic_details(project_id)
        start_date = start_date or project["start_date"]
        end_date = end_date or project["end_date"]
        
        # Optimisation
        allocation = await self.ml_service.optimize_resource_allocation(
            project_id,
            start_date,
            end_date
        )
        
        # Application
        await self._apply_resource_allocation(project_id, allocation)
        
        return allocation

    async def get_project_recommendations(
        self,
        project_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère les recommandations pour un projet"""
        # Analytics
        analytics = await self.get_project_analytics(project_id)
        
        # Génération recommandations
        recommendations = []
        
        # Recommandations performance
        if analytics["performance"]["kpis"]["schedule_performance"] < 0.9:
            recommendations.append({
                "type": "SCHEDULE",
                "priority": "HIGH",
                "description": "Performance planning sous-optimale",
                "actions": analytics["performance"]["recommendations"]
            })
            
        # Recommandations météo
        if analytics["weather_impact"]["impact_score"] > 0.7:
            recommendations.append({
                "type": "WEATHER",
                "priority": "HIGH",
                "description": "Risques météo importants",
                "actions": [
                    f"Reporter {task['task_id']} à {alt['alternative_date']}"
                    for alt in analytics["weather_impact"]["alternatives"]
                    for task in analytics["weather_impact"]["affected_tasks"]
                    if task["task_id"] == alt["task_id"]
                ]
            })
            
        # Recommandations ressources
        if analytics["performance"]["kpis"]["resource_efficiency"] < 0.8:
            recommendations.append({
                "type": "RESOURCE",
                "priority": "MEDIUM",
                "description": "Efficacité ressources sous-optimale",
                "actions": [
                    "Optimiser allocation ressources",
                    "Identifier goulots étranglement"
                ]
            })
            
        return recommendations

    async def _get_basic_details(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """Récupère les détails de base d'un projet"""
        # TODO: Implémenter récupération détails
        return {
            "id": project_id,
            "name": "Project Name",
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31)
        }

    async def _create_basic_project(
        self,
        project_data: Dict[str, Any]
    ) -> Any:
        """Crée un projet de base"""
        # TODO: Implémenter création projet
        return None

    async def _update_basic_project(
        self,
        project_id: str,
        project_data: Dict[str, Any]
    ) -> Any:
        """Met à jour un projet de base"""
        # TODO: Implémenter mise à jour projet
        return None

    async def _apply_resource_allocation(
        self,
        project_id: str,
        allocation: Dict[str, Any]
    ) -> None:
        """Applique une allocation de ressources"""
        # TODO: Implémenter application allocation
        pass

    async def _generate_global_recommendations(
        self,
        project_id: str,
        performance: Dict[str, Any],
        success_prediction: Dict[str, Any],
        weather_impact: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations globales"""
        recommendations = []
        
        # Recommandations performance
        if performance["kpis"]["schedule_performance"] < 0.9:
            recommendations.extend(performance["recommendations"])
            
        # Recommandations succès
        if success_prediction["success_probability"] < 0.8:
            for risk in success_prediction["risk_factors"]:
                recommendations.append({
                    "type": "RISK",
                    "priority": "HIGH",
                    "description": f"Risque: {risk['factor']}",
                    "impact": risk["impact"],
                    "actions": [
                        "Mettre en place plan mitigation",
                        "Renforcer monitoring"
                    ]
                })
                
        # Recommandations météo
        if weather_impact["impact_score"] > 0.7:
            recommendations.extend([
                {
                    "type": "WEATHER",
                    "priority": "HIGH",
                    "description": f"Impact météo sur {task['task_id']}",
                    "actions": [
                        f"Reporter à {alt['alternative_date']}"
                        for alt in weather_impact["alternatives"]
                        if alt["task_id"] == task["task_id"]
                    ]
                }
                for task in weather_impact["affected_tasks"]
            ])
            
        return recommendations
