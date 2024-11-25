"""Service principal d'apprentissage automatique pour les projets."""

from typing import Dict, Any, Optional
from datetime import date
from sqlalchemy.orm import Session

from services.projects_ml import ProjectsML

class ProjectMLService:
    """Service ML pour les projets."""
    
    def __init__(self, db: Session):
        """Initialisation du service."""
        self.projects_ml = ProjectsML(db)

    async def predict_project_success(
        self,
        project_id: str,
        current_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Prédit la probabilité de succès d'un projet."""
        return await self.projects_ml.predict_project_success(
            project_id,
            current_date
        )

    async def optimize_resource_allocation(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Optimise l'allocation des ressources."""
        return await self.projects_ml.optimize_resource_allocation(
            project_id,
            start_date,
            end_date
        )

    async def analyze_project_performance(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse la performance du projet."""
        return await self.projects_ml.analyze_performance(
            project_id,
            start_date,
            end_date
        )

    async def predict_weather_impact(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Prédit l'impact météo sur le projet."""
        return await self.projects_ml.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )
