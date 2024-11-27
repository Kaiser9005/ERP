from fastapi import APIRouter, Depends, HTTPException
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
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les statistiques des employés
    """
    try:
        return await analytics_service.get_employee_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/formation-analytics", response_model=FormationAnalytics)
async def get_formation_analytics(
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des formations
    """
    try:
        return await analytics_service.get_formation_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contract-analytics", response_model=ContractAnalytics)
async def get_contract_analytics(
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des contrats
    """
    try:
        return await analytics_service.get_contract_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payroll-analytics", response_model=PayrollAnalytics)
async def get_payroll_analytics(
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Récupère les analytics des paies
    """
    try:
        return await analytics_service.get_payroll_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict-performance/{employee_id}", response_model=PerformancePrediction)
async def predict_employee_performance(
    employee_id: int,
    analytics_service: HRAnalyticsService = Depends()
):
    """
    Prédit la performance d'un employé
    """
    try:
        prediction = await analytics_service.predict_employee_performance(employee_id)
        if "error" in prediction:
            raise HTTPException(status_code=400, detail=prediction["error"])
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
