from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from services.hr_contract_service import ContractService
from schemas.hr_contract import (
    ContractCreate,
    ContractUpdate,
    ContractResponse,
    ContractInDB
)

router = APIRouter(prefix="/hr/contracts", tags=["contracts"])

@router.post("/", response_model=ContractInDB, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau contrat"""
    try:
        return await ContractService.create_contract(db, contract)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: str,
    db: Session = Depends(get_db)
):
    """Récupère un contrat par son ID"""
    contract = await ContractService.get_contract(db, contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrat non trouvé"
        )
    return contract

@router.get("/employee/{employee_id}", response_model=List[ContractResponse])
async def get_employee_contracts(
    employee_id: str,
    db: Session = Depends(get_db)
):
    """Récupère tous les contrats d'un employé"""
    return await ContractService.get_employee_contracts(db, employee_id)

@router.get("/active", response_model=List[ContractResponse])
async def get_active_contracts(
    db: Session = Depends(get_db)
):
    """Récupère tous les contrats actifs"""
    return await ContractService.get_active_contracts(db)

@router.patch("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: str,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un contrat"""
    updated_contract = await ContractService.update_contract(
        db, contract_id, contract_update
    )
    if not updated_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrat non trouvé"
        )
    return updated_contract

@router.post("/{contract_id}/terminate", response_model=ContractResponse)
async def terminate_contract(
    contract_id: str,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Termine un contrat"""
    terminated_contract = await ContractService.terminate_contract(
        db, contract_id, end_date
    )
    if not terminated_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrat non trouvé ou déjà terminé"
        )
    return terminated_contract

@router.get("/expiring/{days}", response_model=List[ContractResponse])
async def get_expiring_contracts(
    days: int,
    db: Session = Depends(get_db)
):
    """Récupère les contrats qui expirent dans le nombre de jours spécifié"""
    return await ContractService.get_expiring_contracts(db, days)
