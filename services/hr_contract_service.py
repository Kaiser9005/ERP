from datetime import date, timedelta
from typing import List, Optional
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.hr_contract import Contract
from models.hr import Employee
from schemas.hr_contract import ContractCreate, ContractUpdate

class ContractService:
    """Service pour la gestion des contrats"""

    @staticmethod
    async def create_contract(db: Session, contract: ContractCreate) -> Contract:
        """Crée un nouveau contrat"""
        # Vérification de l'existence de l'employé
        employee = db.query(Employee).filter(Employee.id == contract.employee_id).first()
        if not employee:
            raise ValueError("Employé non trouvé")

        # Vérification des contrats actifs existants
        active_contract = db.query(Contract).filter(
            and_(
                Contract.employee_id == contract.employee_id,
                Contract.is_active == True
            )
        ).first()
        
        if active_contract:
            # Désactivation du contrat précédent
            active_contract.is_active = False
            active_contract.end_date = date.today()

        # Création du nouveau contrat
        db_contract = Contract(
            id=str(uuid4()),
            employee_id=contract.employee_id,
            type=contract.type,
            start_date=contract.start_date,
            end_date=contract.end_date,
            wage=contract.wage,
            position=contract.position,
            department=contract.department
        )
        
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract

    @staticmethod
    async def get_contract(db: Session, contract_id: str) -> Optional[Contract]:
        """Récupère un contrat par son ID"""
        return db.query(Contract).filter(Contract.id == contract_id).first()

    @staticmethod
    async def get_employee_contracts(db: Session, employee_id: str) -> List[Contract]:
        """Récupère tous les contrats d'un employé"""
        return db.query(Contract).filter(Contract.employee_id == employee_id).all()

    @staticmethod
    async def get_active_contracts(db: Session) -> List[Contract]:
        """Récupère tous les contrats actifs"""
        return db.query(Contract).filter(Contract.is_active == True).all()

    @staticmethod
    async def update_contract(
        db: Session, 
        contract_id: str, 
        contract_update: ContractUpdate
    ) -> Optional[Contract]:
        """Met à jour un contrat"""
        db_contract = await ContractService.get_contract(db, contract_id)
        if not db_contract:
            return None

        # Mise à jour des champs
        for field, value in contract_update.dict(exclude_unset=True).items():
            setattr(db_contract, field, value)

        db.commit()
        db.refresh(db_contract)
        return db_contract

    @staticmethod
    async def terminate_contract(
        db: Session, 
        contract_id: str, 
        end_date: date
    ) -> Optional[Contract]:
        """Termine un contrat"""
        db_contract = await ContractService.get_contract(db, contract_id)
        if not db_contract or not db_contract.is_active:
            return None

        db_contract.is_active = False
        db_contract.end_date = end_date

        db.commit()
        db.refresh(db_contract)
        return db_contract

    @staticmethod
    async def get_expiring_contracts(db: Session, days: int) -> List[Contract]:
        """Récupère les contrats qui expirent dans le nombre de jours spécifié"""
        target_date = date.today() + timedelta(days=days)
        return db.query(Contract).filter(
            and_(
                Contract.is_active == True,
                Contract.end_date <= target_date,
                Contract.end_date > date.today()
            )
        ).all()
