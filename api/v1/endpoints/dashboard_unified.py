from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session

from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.ml.projets.service import ProjetsMLService
from services.cache_service import CacheService
from db.database import get_db

router = APIRouter()

async def get_dashboard_service(db: Session = Depends(get_db)):
    """Injection des dépendances pour le service dashboard unifié."""
    return TableauBordUnifieService(
        hr_service=HRAnalyticsService(),
        production_service=ProductionService(),
        finance_service=FinanceService(),
        inventory_service=InventoryService(),
        weather_service=WeatherService(),
        projets_ml=ProjetsMLService(db),
        cache_service=CacheService()
    )

@router.get("/unified", response_model=Dict[str, Any])
async def get_unified_dashboard(
    service: TableauBordUnifieService = Depends(get_dashboard_service)
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

@router.get("/module/{module}", response_model=Dict[str, Any])
async def get_module_details(
    module: str,
    service: TableauBordUnifieService = Depends(get_dashboard_service)
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
