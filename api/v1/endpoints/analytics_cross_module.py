"""
API endpoints pour les analytics cross-module
"""

from typing import Dict, Any, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.security import get_current_user, Permission, require_permissions
from db.database import get_db
from services.analytics_cross_module_service import CrossModuleAnalytics

router = APIRouter()

@router.get("/analytics/cross-module/unified")
async def get_unified_analytics(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Récupère les analytics unifiés de tous les modules.
    Inclut les corrélations et prédictions cross-module.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service.get_unified_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des analytics: {str(e)}"
        )

@router.get("/analytics/cross-module/correlations")
async def get_correlations(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Récupère les corrélations entre les différents modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._analyze_correlations(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse des corrélations: {str(e)}"
        )

@router.get("/analytics/cross-module/predictions")
async def get_predictions(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Récupère les prédictions ML cross-module.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_ml_predictions(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des prédictions: {str(e)}"
        )

@router.get("/analytics/cross-module/recommendations")
async def get_recommendations(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Récupère les recommandations cross-module basées sur ML.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._generate_cross_module_recommendations(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération des recommandations: {str(e)}"
        )

@router.get("/analytics/cross-module/hr-impact")
async def get_hr_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact RH sur les autres modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_hr_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact RH: {str(e)}"
        )

@router.get("/analytics/cross-module/production-impact")
async def get_production_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact production sur les autres modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_production_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact production: {str(e)}"
        )

@router.get("/analytics/cross-module/finance-impact")
async def get_finance_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact finance sur les autres modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_finance_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact finance: {str(e)}"
        )

@router.get("/analytics/cross-module/inventory-impact")
async def get_inventory_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact inventaire sur les autres modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_inventory_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact inventaire: {str(e)}"
        )

@router.get("/analytics/cross-module/weather-impact")
async def get_weather_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact météo sur tous les modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_weather_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact météo: {str(e)}"
        )

@router.get("/analytics/cross-module/projects-impact")
async def get_projects_impact(
    date_debut: Optional[date] = Query(None, description="Date de début de l'analyse"),
    date_fin: Optional[date] = Query(None, description="Date de fin de l'analyse"),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Analyse l'impact des projets sur tous les modules.
    """
    try:
        service = CrossModuleAnalytics(db)
        return await service._get_projects_analytics(date_debut, date_fin)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de l'impact des projets: {str(e)}"
        )
