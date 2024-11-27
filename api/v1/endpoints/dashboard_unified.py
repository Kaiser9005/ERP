from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from services.dashboard_unified_service import DashboardUnifiedService
from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.projects_ml_service import ProjectsMLService
from services.cache_service import CacheService

router = APIRouter()

async def get_dashboard_service():
    """Injection des dépendances pour le service dashboard unifié."""
    return DashboardUnifiedService(
        hr_service=HRAnalyticsService(),
        production_service=ProductionService(),
        finance_service=FinanceService(),
        inventory_service=InventoryService(),
        weather_service=WeatherService(),
        projects_ml_service=ProjectsMLService(),
        cache_service=CacheService()
    )

@router.get("/dashboard/unified", response_model=Dict[str, Any])
async def get_unified_dashboard(
    service: DashboardUnifiedService = Depends(get_dashboard_service)
) -> Dict[str, Any]:
    """
    Récupère les données du dashboard unifié.
    
    Returns:
        Dict[str, Any]: Données agrégées de tous les modules
    """
    try:
        return await service.get_unified_dashboard_data()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des données du dashboard: {str(e)}"
        )

@router.get("/dashboard/module/{module}", response_model=Dict[str, Any])
async def get_module_details(
    module: str,
    service: DashboardUnifiedService = Depends(get_dashboard_service)
) -> Dict[str, Any]:
    """
    Récupère les détails d'un module spécifique.
    
    Args:
        module: Nom du module (hr, production, finance, inventory, weather, projects)
        
    Returns:
        Dict[str, Any]: Données détaillées du module
    """
    try:
        return await service.get_module_details(module)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des détails du module: {str(e)}"
        )
