"""Module d'apprentissage automatique pour les projets."""

from typing import Dict, Any, List, Optional
from datetime import date
from sqlalchemy.orm import Session

from .base import ProjectsMLService
from .optimization import ResourceOptimizer
from .analysis import PerformanceAnalyzer
from .weather import WeatherAnalyzer

class ProjectsML:
    """Interface principale du module ML des projets."""
    
    def __init__(self, db: Session):
        """Initialisation des services."""
        self.db = db
        self._ml_service = ProjectsMLService(db)
        self._optimizer = ResourceOptimizer(db)
        self._analyzer = PerformanceAnalyzer(db)
        self._weather = WeatherAnalyzer(db)

    async def predict_project_success(
        self,
        project_id: str,
        current_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Prédit la probabilité de succès d'un projet."""
        return await self._ml_service.predict_project_success(
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
        return await self._optimizer.optimize_allocation(
            project_id,
            start_date,
            end_date
        )

    async def analyze_performance(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse la performance du projet."""
        return await self._analyzer.analyze_performance(
            project_id,
            start_date,
            end_date
        )

    async def analyze_weather_impact(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Analyse l'impact météo sur le projet."""
        return await self._weather.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )

__all__ = ['ProjectsML']
