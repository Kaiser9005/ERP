from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from db.database import get_db
from models.auth import Utilisateur
from api.v1.endpoints.auth import get_current_user
from services.dashboard_service import DashboardService
from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.ml.projets.service import ProjetsMLService
from services.cache_service import CacheService

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
) -> Dict[str, Any]:
    """Récupère les statistiques pour le tableau de bord"""
    dashboard_service = DashboardService(db)
    return await dashboard_service.get_stats()

@router.get("/activities")
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les activités récentes"""
    dashboard_service = DashboardService(db)
    return await dashboard_service.get_recent_activities(limit)

@router.get("/weather")
async def get_weather_data(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les données météorologiques"""
    dashboard_service = DashboardService(db)
    return await dashboard_service.get_weather_data()

@router.get("/unified")
async def get_unified_dashboard(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
) -> Dict[str, Any]:
    """Récupère les données du tableau de bord unifié"""
    service = TableauBordUnifieService(
        hr_service=HRAnalyticsService(db),
        production_service=ProductionService(db),
        finance_service=FinanceService(db),
        inventory_service=InventoryService(db),
        weather_service=WeatherService(db),
        projets_ml=ProjetsMLService(db),
        cache_service=CacheService()
    )
    return await service.get_unified_dashboard_data()