from datetime import date
import pytest
from sqlalchemy.orm import Session
from uuid import uuid4

from models.hr_payroll import Payroll
from models.hr_contract import Contract
from models.hr import Employee
from services.hr_payroll_service import PayrollService
from schemas.hr_payroll import PayrollCreate, PayrollUpdate

@pytest.fixture
def employee(db: Session):
    """Fixture pour créer un employé de test"""
    employee = Employee(
        id=str(uuid4()),
        name="Jean Test",
        email="jean.test@example.com"
    )
    db.add(employee)
    db.commit()
    return employee

@pytest.fixture
def contract(db: Session, employee: Employee):
    """Fixture pour créer un contrat de test"""
    contract = Contract(
        id=str(uuid4()),
        employee_id=employee.id,
        type="CDI",
        start_date=date(2024, 1, 1),
        wage=2000.0,
        position="Agriculteur",
        department="Production",
        is_active=True
    )
    db.add(contract)
    db.commit()
    return contract

@pytest.fixture
def payroll_service(db: Session):
    """Fixture pour le service de paie"""
    return PayrollService(db)

def test_create_payroll_integration(db: Session, contract: Contract, payroll_service: PayrollService):
    """Test d'intégration de la création d'une fiche de paie"""
    # Création de la fiche de paie
    payroll_data = PayrollCreate(
        contract_id=contract.id,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        worked_hours=151.67,
        overtime_hours=10.0,
        overtime_amount=250.0,
        bonus=100.0,
        deductions=50.0,
        bonus_details={"prime_agricole": 100.0},
        deduction_details={"absence": 50.0},
        employer_contributions=500.0,
        employee_contributions=200.0
    )

    # Création via le service
    payroll = payroll_service.create_payroll(payroll_data)

    # Vérification en base
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll.id).first()
    assert db_payroll is not None
    assert db_payroll.contract_id == contract.id
    assert db_payroll.base_salary == contract.wage
    assert db_payroll.worked_hours == payroll_data.worked_hours
    assert db_payroll.overtime_hours == payroll_data.overtime_hours
    assert db_payroll.overtime_amount == payroll_data.overtime_amount
    assert db_payroll.bonus == payroll_data.bonus
    assert db_payroll.deductions == payroll_data.deductions

def test_update_payroll_integration(db: Session, contract: Contract, payroll_service: PayrollService):
    """Test d'intégration de la mise à jour d'une fiche de paie"""
    # Création initiale
    payroll = Payroll(
        id=str(uuid4()),
        contract_id=contract.id,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        worked_hours=151.67,
        overtime_hours=10.0,
        base_salary=contract.wage
    )
    db.add(payroll)
    db.commit()

    # Mise à jour
    update_data = PayrollUpdate(
        worked_hours=160.0,
        overtime_hours=15.0,
        overtime_amount=375.0
    )

    updated_payroll = payroll_service.update_payroll(payroll.id, update_data)

    # Vérification en base
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll.id).first()
    assert db_payroll.worked_hours == update_data.worked_hours
    assert db_payroll.overtime_hours == update_data.overtime_hours
    assert db_payroll.overtime_amount == update_data.overtime_amount

def test_validate_payroll_integration(db: Session, contract: Contract, payroll_service: PayrollService):
    """Test d'intégration de la validation d'une fiche de paie"""
    # Création initiale
    payroll = Payroll(
        id=str(uuid4()),
        contract_id=contract.id,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        worked_hours=151.67,
        base_salary=contract.wage,
        is_paid=False
    )
    db.add(payroll)
    db.commit()

    # Validation
    result = payroll_service.validate_payroll(payroll.id)
    assert result is True

    # Vérification en base
    db_payroll = db.query(Payroll).filter(Payroll.id == payroll.id).first()
    assert db_payroll.is_paid is True
    assert db_payroll.payment_date is not None

def test_get_payrolls_by_contract_integration(db: Session, contract: Contract, payroll_service: PayrollService):
    """Test d'intégration de la récupération des fiches de paie par contrat"""
    # Création de plusieurs fiches de paie
    payrolls = []
    for month in range(1, 4):  # 3 mois
        payroll = Payroll(
            id=str(uuid4()),
            contract_id=contract.id,
            period_start=date(2024, month, 1),
            period_end=date(2024, month, 31),
            worked_hours=151.67,
            base_salary=contract.wage
        )
        payrolls.append(payroll)
        db.add(payroll)
    db.commit()

    # Récupération via le service
    result = payroll_service.get_payrolls_by_contract(contract.id)
    
    assert len(result) == 3
    for payroll in result:
        assert payroll.contract_id == contract.id

def test_get_payroll_stats_integration(db: Session, contract: Contract, payroll_service: PayrollService):
    """Test d'intégration des statistiques de paie"""
    # Création de fiches de paie pour la période
    for month in range(1, 4):  # 3 mois
        payroll = Payroll(
            id=str(uuid4()),
            contract_id=contract.id,
            period_start=date(2024, month, 1),
            period_end=date(2024, month, 31),
            worked_hours=151.67,
            base_salary=2000.0,
            gross_total=2500.0,
            net_total=2000.0,
            employer_contributions=500.0,
            employee_contributions=200.0,
            bonus=100.0,
            deductions=50.0
        )
        db.add(payroll)
    db.commit()

    # Calcul des stats
    stats = payroll_service.get_payroll_stats(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31)
    )

    # Vérifications
    assert stats.total_gross == 7500.0  # 2500 * 3
    assert stats.total_net == 6000.0    # 2000 * 3
    assert stats.total_employer_contributions == 1500.0  # 500 * 3
    assert stats.total_employee_contributions == 600.0   # 200 * 3
    assert stats.total_bonus == 300.0   # 100 * 3
    assert stats.total_deductions == 150.0  # 50 * 3
    assert stats.average_gross == 2500.0
    assert stats.average_net == 2000.0
