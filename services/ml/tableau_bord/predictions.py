"""
Service de prédictions ML pour le tableau de bord.
"""

from typing import Dict, Any
from services.projects_ml_service import ProjectsMLService

async def get_ml_predictions(projects_ml_service: ProjectsMLService) -> Dict[str, Any]:
    """Agrège les prédictions ML de tous les modules."""
    return {
        "production": await projects_ml_service.get_production_predictions(),
        "finance": await projects_ml_service.get_finance_predictions(),
        "inventory": await projects_ml_service.get_inventory_predictions(),
        "hr": await projects_ml_service.get_hr_predictions()
    }
