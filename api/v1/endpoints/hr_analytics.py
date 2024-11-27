from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Dict, Any

from db.database import get_db
from services.hr_analytics_service import HRAnalyticsService
from schemas.hr_analytics import (
    HRAnalytics,
    EmployeeStats,
    FormationAnalytics,
    ContractAnalytics,
    PayrollAnalytics,
    PerformancePrediction
)

router = APIRouter(
    prefix="/api/v1/hr/analytics",
    tags=["hr-analytics"],
    responses={404: {"description": "Non trouvé"}}
)

@router.get("/", response_model=HRAnalytics)
async def get_hr_analytics(
    response: Response,
    db: Session = Depends(get_db),
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère toutes les analytics RH
    """
    try:
        employee_stats = await analytics_service.get_employee_stats()
        formation_analytics = await analytics_service.get_formation_analytics()
        contract_analytics = await analytics_service.get_contract_analytics()
        payroll_analytics = await analytics_service.get_payroll_analytics()

        # Configuration du cache
        response.headers["Cache-Control"] = "public, max-age=900"  # 15 minutes

        return HRAnalytics(
            employee_stats=EmployeeStats(**employee_stats),
            formation_analytics=FormationAnalytics(**formation_analytics),
            contract_analytics=ContractAnalytics(**contract_analytics),
            payroll_analytics=PayrollAnalytics(**payroll_analytics)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employee-stats", response_model=EmployeeStats)
async def get_employee_stats(
    response: Response,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les statistiques des employés
    """
    try:
        stats = await analytics_service.get_employee_stats()
        response.headers["Cache-Control"] = "public, max-age=900"  # 15 minutes
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/formation-analytics", response_model=FormationAnalytics)
async def get_formation_analytics(
    response: Response,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des formations
    """
    try:
        analytics = await analytics_service.get_formation_analytics()
        response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutes
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contract-analytics", response_model=ContractAnalytics)
async def get_contract_analytics(
    response: Response,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des contrats
    """
    try:
        analytics = await analytics_service.get_contract_analytics()
        response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutes
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payroll-analytics", response_model=PayrollAnalytics)
async def get_payroll_analytics(
    response: Response,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des paies
    """
    try:
        analytics = await analytics_service.get_payroll_analytics()
        response.headers["Cache-Control"] = "public, max-age=1800"  # 30 minutes
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict-performance/{employee_id}", response_model=PerformancePrediction)
async def predict_employee_performance(
    employee_id: int,
    response: Response,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Prédit la performance d'un employé
    """
    try:
        prediction = await analytics_service.predict_employee_performance(employee_id)
        if "error" in prediction:
            raise HTTPException(status_code=400, detail=prediction["error"])
        response.headers["Cache-Control"] = "public, max-age=3600"  # 1 heure
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cache/invalidate")
async def invalidate_cache(
    employee_id: int = None,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Invalide le cache des analytics RH
    
    - Si employee_id est fourni, invalide uniquement le cache pour cet employé
    - Sinon, invalide tout le cache des analytics RH
    """
    try:
        await analytics_service.invalidate_employee_cache(employee_id)
        return {"message": "Cache invalidé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
