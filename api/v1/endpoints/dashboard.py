from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from db.database import get_db
from models.auth import Utilisateur
from api.v1.endpoints.auth import get_current_user
from services.dashboard_service import DashboardService

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