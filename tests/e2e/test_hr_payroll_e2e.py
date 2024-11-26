import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from main import app
from models.hr import Employee
from models.hr_contract import Contract
from models.hr_payroll import Payroll

@pytest.fixture
def client():
    """Client de test FastAPI"""
    return TestClient(app)

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

def test_create_payroll_e2e(client: TestClient, contract: Contract):
    """Test E2E de création d'une fiche de paie"""
    # Données de la fiche de paie
    payroll_data = {
        "contract_id": contract.id,
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
        "worked_hours": 151.67,
        "overtime_hours": 10.0,
        "overtime_amount": 250.0,
        "bonus": 100.0,
        "deductions": 50.0,
        "bonus_details": {"prime_agricole": 100.0},
        "deduction_details": {"absence": 50.0},
        "employer_contributions": 500.0,
        "employee_contributions": 200.0
    }

    # Création via l'API
    response = client.post("/api/v1/payroll", json=payroll_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["contract_id"] == contract.id
    assert result["base_salary"] == contract.wage
    assert result["worked_hours"] == payroll_data["worked_hours"]
    assert result["overtime_hours"] == payroll_data["overtime_hours"]
    assert result["overtime_amount"] == payroll_data["overtime_amount"]
    assert result["bonus"] == payroll_data["bonus"]
    assert result["deductions"] == payroll_data["deductions"]
    assert not result["is_paid"]

def test_payroll_workflow_e2e(client: TestClient, contract: Contract):
    """Test E2E du workflow complet de paie"""
    # 1. Création de la fiche de paie
    payroll_data = {
        "contract_id": contract.id,
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
        "worked_hours": 151.67,
        "overtime_hours": 10.0,
        "overtime_amount": 250.0,
        "bonus": 100.0,
        "deductions": 50.0,
        "bonus_details": {"prime_agricole": 100.0},
        "deduction_details": {"absence": 50.0},
        "employer_contributions": 500.0,
        "employee_contributions": 200.0
    }

    response = client.post("/api/v1/payroll", json=payroll_data)
    assert response.status_code == 200
    payroll_id = response.json()["id"]

    # 2. Mise à jour des heures supplémentaires
    update_data = {
        "overtime_hours": 15.0,
        "overtime_amount": 375.0
    }
    response = client.patch(f"/api/v1/payroll/{payroll_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["overtime_hours"] == 15.0
    assert response.json()["overtime_amount"] == 375.0

    # 3. Calcul des cotisations
    response = client.post(f"/api/v1/payroll/{payroll_id}/calculate-contributions")
    assert response.status_code == 200
    contributions = response.json()
    assert "employer" in contributions
    assert "employee" in contributions

    # 4. Validation de la fiche de paie
    response = client.post(f"/api/v1/payroll/{payroll_id}/validate")
    assert response.status_code == 200
    
    # 5. Vérification de l'état final
    response = client.get(f"/api/v1/payroll/{payroll_id}")
    assert response.status_code == 200
    final_state = response.json()
    assert final_state["is_paid"]
    assert final_state["payment_date"] is not None

def test_payroll_stats_e2e(client: TestClient, db: Session, contract: Contract):
    """Test E2E des statistiques de paie"""
    # Création de plusieurs fiches de paie
    for month in range(1, 4):  # 3 mois
        payroll_data = {
            "contract_id": contract.id,
            "period_start": f"2024-{month:02d}-01",
            "period_end": f"2024-{month:02d}-31",
            "worked_hours": 151.67,
            "overtime_hours": 10.0,
            "overtime_amount": 250.0,
            "bonus": 100.0,
            "deductions": 50.0,
            "employer_contributions": 500.0,
            "employee_contributions": 200.0
        }
        client.post("/api/v1/payroll", json=payroll_data)

    # Récupération des statistiques
    response = client.get(
        "/api/v1/payroll/stats",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-03-31"
        }
    )
    assert response.status_code == 200
    
    stats = response.json()
    assert len(stats) > 0
    assert stats["total_gross"] > 0
    assert stats["total_net"] > 0
    assert stats["average_gross"] > 0
    assert stats["average_net"] > 0

def test_error_handling_e2e(client: TestClient):
    """Test E2E de la gestion des erreurs"""
    # 1. Contrat invalide
    payroll_data = {
        "contract_id": str(uuid4()),  # ID inexistant
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
        "worked_hours": 151.67
    }
    response = client.post("/api/v1/payroll", json=payroll_data)
    assert response.status_code == 400

    # 2. Fiche de paie inexistante
    response = client.get(f"/api/v1/payroll/{uuid4()}")
    assert response.status_code == 404

    # 3. Validation d'une fiche inexistante
    response = client.post(f"/api/v1/payroll/{uuid4()}/validate")
    assert response.status_code == 404

    # 4. Mise à jour d'une fiche inexistante
    response = client.patch(
        f"/api/v1/payroll/{uuid4()}",
        json={"worked_hours": 160.0}
    )
    assert response.status_code == 404
