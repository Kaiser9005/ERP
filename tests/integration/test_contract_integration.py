import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient

from models.hr_contract import Contract
from models.hr import Employee
from services.hr_contract_service import ContractService
from schemas.hr_contract import ContractCreate, ContractUpdate

@pytest.fixture
def test_employee(db: Session):
    """Crée un employé de test"""
    employee = Employee(
        id="test_emp",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com"
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@pytest.fixture
def test_contract(db: Session, test_employee):
    """Crée un contrat de test"""
    contract = Contract(
        id="test_contract",
        employee_id=test_employee.id,
        type="CDI",
        start_date=date.today(),
        wage=2500,
        position="Agriculteur",
        department="Production",
        is_active=True,
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

class TestContractIntegration:
    async def test_create_contract(self, db: Session, test_employee):
        """Teste la création d'un contrat"""
        contract_data = ContractCreate(
            employee_id=test_employee.id,
            type="CDI",
            start_date=date.today(),
            wage=2500,
            position="Agriculteur",
            department="Production"
        )

        contract = await ContractService.create_contract(db, contract_data)

        assert contract.employee_id == test_employee.id
        assert contract.type == "CDI"
        assert contract.wage == 2500
        assert contract.is_active == True

    async def test_get_contract(self, db: Session, test_contract):
        """Teste la récupération d'un contrat"""
        contract = await ContractService.get_contract(db, test_contract.id)

        assert contract is not None
        assert contract.id == test_contract.id
        assert contract.employee_id == test_contract.employee_id

    async def test_get_employee_contracts(self, db: Session, test_employee, test_contract):
        """Teste la récupération des contrats d'un employé"""
        contracts = await ContractService.get_employee_contracts(db, test_employee.id)

        assert len(contracts) == 1
        assert contracts[0].id == test_contract.id
        assert contracts[0].employee_id == test_employee.id

    async def test_get_active_contracts(self, db: Session, test_contract):
        """Teste la récupération des contrats actifs"""
        contracts = await ContractService.get_active_contracts(db)

        assert len(contracts) > 0
        assert any(c.id == test_contract.id for c in contracts)

    async def test_update_contract(self, db: Session, test_contract):
        """Teste la mise à jour d'un contrat"""
        update_data = ContractUpdate(
            wage=3000,
            position="Chef d'équipe"
        )

        updated_contract = await ContractService.update_contract(
            db, test_contract.id, update_data
        )

        assert updated_contract is not None
        assert updated_contract.wage == 3000
        assert updated_contract.position == "Chef d'équipe"

    async def test_terminate_contract(self, db: Session, test_contract):
        """Teste la terminaison d'un contrat"""
        end_date = date.today()
        terminated_contract = await ContractService.terminate_contract(
            db, test_contract.id, end_date
        )

        assert terminated_contract is not None
        assert terminated_contract.is_active == False
        assert terminated_contract.end_date == end_date

    async def test_get_expiring_contracts(self, db: Session, test_employee):
        """Teste la récupération des contrats qui expirent bientôt"""
        # Créer un contrat qui expire dans 15 jours
        expiring_contract = Contract(
            id="expiring_contract",
            employee_id=test_employee.id,
            type="CDD",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=15),
            wage=2500,
            position="Agriculteur",
            department="Production",
            is_active=True,
            created_at=date.today(),
            updated_at=date.today()
        )
        db.add(expiring_contract)
        db.commit()

        # Vérifier les contrats qui expirent dans 30 jours
        expiring_contracts = await ContractService.get_expiring_contracts(db, 30)

        assert len(expiring_contracts) > 0
        assert any(c.id == expiring_contract.id for c in expiring_contracts)

    async def test_create_contract_invalid_employee(self, db: Session):
        """Teste la création d'un contrat avec un employé invalide"""
        contract_data = ContractCreate(
            employee_id="invalid_id",
            type="CDI",
            start_date=date.today(),
            wage=2500,
            position="Agriculteur",
            department="Production"
        )

        with pytest.raises(ValueError, match="Employé non trouvé"):
            await ContractService.create_contract(db, contract_data)

    async def test_update_nonexistent_contract(self, db: Session):
        """Teste la mise à jour d'un contrat inexistant"""
        update_data = ContractUpdate(wage=3000)
        
        result = await ContractService.update_contract(
            db, "nonexistent_id", update_data
        )

        assert result is None

    async def test_terminate_inactive_contract(self, db: Session, test_contract):
        """Teste la terminaison d'un contrat déjà inactif"""
        # D'abord terminer le contrat
        end_date = date.today()
        await ContractService.terminate_contract(db, test_contract.id, end_date)

        # Essayer de le terminer à nouveau
        result = await ContractService.terminate_contract(
            db, test_contract.id, end_date
        )

        assert result is None

    async def test_multiple_active_contracts(self, db: Session, test_employee):
        """Teste la gestion de plusieurs contrats actifs pour un même employé"""
        # Créer un premier contrat actif
        contract1_data = ContractCreate(
            employee_id=test_employee.id,
            type="CDI",
            start_date=date.today(),
            wage=2500,
            position="Agriculteur",
            department="Production"
        )
        contract1 = await ContractService.create_contract(db, contract1_data)

        # Créer un deuxième contrat actif
        contract2_data = ContractCreate(
            employee_id=test_employee.id,
            type="CDI",
            start_date=date.today(),
            wage=3000,
            position="Chef d'équipe",
            department="Production"
        )
        contract2 = await ContractService.create_contract(db, contract2_data)

        # Vérifier que le premier contrat est maintenant inactif
        db.refresh(contract1)
        assert contract1.is_active == False
        assert contract2.is_active == True
