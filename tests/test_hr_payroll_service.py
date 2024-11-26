from datetime import date
from unittest.mock import Mock
import pytest
from uuid import uuid4

from models.hr_payroll import Payroll
from models.hr_contract import Contract
from services.hr_payroll_service import PayrollService
from schemas.hr_payroll import PayrollCreate, PayrollUpdate

@pytest.fixture
def db_session():
    """Mock de session de base de données"""
    return Mock()

@pytest.fixture
def contract():
    """Fixture de contrat"""
    return Contract(
        id=str(uuid4()),
        employee_id=str(uuid4()),
        type="CDI",
        start_date=date(2024, 1, 1),
        wage=2000.0,
        position="Agriculteur",
        department="Production",
        is_active=True
    )

@pytest.fixture
def payroll_create():
    """Fixture de création de paie"""
    return PayrollCreate(
        contract_id=str(uuid4()),
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

def test_create_payroll(db_session, contract, payroll_create):
    """Test la création d'une fiche de paie"""
    # Setup
    db_session.query.return_value.filter.return_value.first.return_value = contract
    service = PayrollService(db_session)

    # Exécution
    result = service.create_payroll(payroll_create)

    # Vérifications
    assert result.contract_id == payroll_create.contract_id
    assert result.period_start == payroll_create.period_start
    assert result.period_end == payroll_create.period_end
    assert result.worked_hours == payroll_create.worked_hours
    assert result.overtime_hours == payroll_create.overtime_hours
    assert result.overtime_amount == payroll_create.overtime_amount
    assert result.bonus == payroll_create.bonus
    assert result.deductions == payroll_create.deductions
    assert result.bonus_details == payroll_create.bonus_details
    assert result.deduction_details == payroll_create.deduction_details
    assert result.employer_contributions == payroll_create.employer_contributions
    assert result.employee_contributions == payroll_create.employee_contributions
    assert result.base_salary == contract.wage
    assert not result.is_paid
    assert result.payment_date is None

def test_create_payroll_invalid_contract(db_session, payroll_create):
    """Test la création avec un contrat invalide"""
    # Setup
    db_session.query.return_value.filter.return_value.first.return_value = None
    service = PayrollService(db_session)

    # Vérification
    with pytest.raises(ValueError):
        service.create_payroll(payroll_create)

def test_create_payroll_inactive_contract(db_session, contract, payroll_create):
    """Test la création avec un contrat inactif"""
    # Setup
    contract.is_active = False
    db_session.query.return_value.filter.return_value.first.return_value = contract
    service = PayrollService(db_session)

    # Vérification
    with pytest.raises(ValueError):
        service.create_payroll(payroll_create)

def test_get_payroll(db_session):
    """Test la récupération d'une fiche de paie"""
    # Setup
    payroll_id = str(uuid4())
    payroll = Payroll(id=payroll_id)
    db_session.query.return_value.filter.return_value.first.return_value = payroll
    service = PayrollService(db_session)

    # Exécution
    result = service.get_payroll(payroll_id)

    # Vérification
    assert result == payroll

def test_get_payrolls_by_contract(db_session):
    """Test la récupération des fiches de paie d'un contrat"""
    # Setup
    contract_id = str(uuid4())
    payrolls = [Payroll(id=str(uuid4())) for _ in range(3)]
    db_session.query.return_value.filter.return_value.all.return_value = payrolls
    service = PayrollService(db_session)

    # Exécution
    result = service.get_payrolls_by_contract(contract_id)

    # Vérification
    assert result == payrolls

def test_get_payrolls_by_period(db_session):
    """Test la récupération des fiches de paie par période"""
    # Setup
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    payrolls = [Payroll(id=str(uuid4())) for _ in range(3)]
    db_session.query.return_value.filter.return_value.all.return_value = payrolls
    service = PayrollService(db_session)

    # Exécution
    result = service.get_payrolls_by_period(start_date, end_date)

    # Vérification
    assert result == payrolls

def test_update_payroll(db_session):
    """Test la mise à jour d'une fiche de paie"""
    # Setup
    payroll = Payroll(
        id=str(uuid4()),
        worked_hours=151.67,
        overtime_hours=10.0
    )
    db_session.query.return_value.filter.return_value.first.return_value = payroll
    service = PayrollService(db_session)
    update = PayrollUpdate(worked_hours=160.0, overtime_hours=15.0)

    # Exécution
    result = service.update_payroll(payroll.id, update)

    # Vérification
    assert result.worked_hours == update.worked_hours
    assert result.overtime_hours == update.overtime_hours

def test_validate_payroll(db_session):
    """Test la validation d'une fiche de paie"""
    # Setup
    payroll = Payroll(id=str(uuid4()), is_paid=False)
    db_session.query.return_value.filter.return_value.first.return_value = payroll
    service = PayrollService(db_session)

    # Exécution
    result = service.validate_payroll(payroll.id)

    # Vérification
    assert result is True
    assert payroll.is_paid is True
    assert isinstance(payroll.payment_date, date)

def test_calculate_overtime():
    """Test le calcul des heures supplémentaires"""
    # Setup
    service = PayrollService(Mock())
    hours = 10.0
    base_rate = 13.0  # SMIC horaire approximatif

    # Exécution
    result = service.calculate_overtime(hours, base_rate)

    # Vérification
    assert result == hours * base_rate * 1.25  # Majoration de 25%

def test_calculate_contributions():
    """Test le calcul des cotisations"""
    # Setup
    service = PayrollService(Mock())
    gross_amount = 2000.0

    # Exécution
    result = service.calculate_contributions(gross_amount)

    # Vérification
    assert result["employer"] == gross_amount * 0.45  # 45% charges patronales
    assert result["employee"] == gross_amount * 0.22  # 22% charges salariales
