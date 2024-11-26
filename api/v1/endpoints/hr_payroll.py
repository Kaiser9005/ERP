from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from services.hr_payroll_service import PayrollService
from schemas.hr_payroll import (
    PayrollCreate,
    PayrollUpdate,
    PayrollResponse,
    PayrollStats
)

router = APIRouter(
    prefix="/api/v1/payroll",
    tags=["payroll"]
)

@router.post("", response_model=PayrollResponse)
def create_payroll(
    payroll: PayrollCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle fiche de paie"""
    try:
        service = PayrollService(db)
        return service.create_payroll(payroll)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{payroll_id}", response_model=PayrollResponse)
def get_payroll(
    payroll_id: str,
    db: Session = Depends(get_db)
):
    """Récupère une fiche de paie par son ID"""
    service = PayrollService(db)
    payroll = service.get_payroll(payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    return payroll

@router.get("/contract/{contract_id}", response_model=List[PayrollResponse])
def get_payrolls_by_contract(
    contract_id: str,
    db: Session = Depends(get_db)
):
    """Récupère toutes les fiches de paie d'un contrat"""
    service = PayrollService(db)
    return service.get_payrolls_by_contract(contract_id)

@router.get("/period", response_model=List[PayrollResponse])
def get_payrolls_by_period(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Récupère les fiches de paie pour une période donnée"""
    service = PayrollService(db)
    return service.get_payrolls_by_period(start_date, end_date)

@router.patch("/{payroll_id}", response_model=PayrollResponse)
def update_payroll(
    payroll_id: str,
    payroll_update: PayrollUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une fiche de paie"""
    service = PayrollService(db)
    payroll = service.update_payroll(payroll_id, payroll_update)
    if not payroll:
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    return payroll

@router.post("/{payroll_id}/validate")
def validate_payroll(
    payroll_id: str,
    db: Session = Depends(get_db)
):
    """Valide une fiche de paie pour paiement"""
    service = PayrollService(db)
    if not service.validate_payroll(payroll_id):
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    return {"message": "Fiche de paie validée"}

@router.delete("/{payroll_id}")
def delete_payroll(
    payroll_id: str,
    db: Session = Depends(get_db)
):
    """Supprime une fiche de paie"""
    service = PayrollService(db)
    if not service.delete_payroll(payroll_id):
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    return {"message": "Fiche de paie supprimée"}

@router.get("/stats", response_model=PayrollStats)
def get_payroll_stats(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Récupère les statistiques de paie pour une période"""
    service = PayrollService(db)
    return service.get_payroll_stats(start_date, end_date)

@router.post("/{payroll_id}/calculate-overtime")
def calculate_overtime(
    payroll_id: str,
    hours: float,
    db: Session = Depends(get_db)
):
    """Calcule le montant des heures supplémentaires"""
    service = PayrollService(db)
    payroll = service.get_payroll(payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    
    # Calcul basé sur le salaire horaire du contrat
    hourly_rate = payroll.contract.wage / 151.67  # 151.67 = heures mensuelles pour 35h/semaine
    overtime_amount = service.calculate_overtime(hours, hourly_rate)
    
    return {
        "overtime_hours": hours,
        "overtime_amount": overtime_amount
    }

@router.post("/{payroll_id}/calculate-contributions")
def calculate_contributions(
    payroll_id: str,
    db: Session = Depends(get_db)
):
    """Calcule les cotisations sociales"""
    service = PayrollService(db)
    payroll = service.get_payroll(payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="Fiche de paie non trouvée")
    
    contributions = service.calculate_contributions(payroll.gross_total)
    return contributions
