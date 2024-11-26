import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.hr import Employee
from models.hr_contract import Contract

def create_test_employee(db: Session) -> Employee:
    """Crée un employé de test dans la base de données"""
    employee = Employee(
        id="test_emp_e2e",
        first_name="John",
        last_name="Doe",
        email="john.doe.e2e@example.com"
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def create_test_contract(db: Session, employee_id: str) -> Contract:
    """Crée un contrat de test dans la base de données"""
    contract = Contract(
        id="test_contract_e2e",
        employee_id=employee_id,
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

class TestContractManagementE2E:
    """Tests end-to-end pour la gestion des contrats"""

    def test_contract_lifecycle(self, client: TestClient, db: Session):
        """Test du cycle de vie complet d'un contrat"""
        # 1. Créer un employé
        employee = create_test_employee(db)

        # 2. Créer un contrat
        contract_data = {
            "employee_id": employee.id,
            "type": "CDI",
            "start_date": date.today().isoformat(),
            "wage": 2500,
            "position": "Agriculteur",
            "department": "Production"
        }
        response = client.post("/hr/contracts", json=contract_data)
        assert response.status_code == 201
        contract_id = response.json()["id"]

        # 3. Vérifier que le contrat a été créé
        response = client.get(f"/hr/contracts/{contract_id}")
        assert response.status_code == 200
        contract = response.json()
        assert contract["employee_id"] == employee.id
        assert contract["type"] == "CDI"
        assert contract["is_active"] == True

        # 4. Mettre à jour le contrat
        update_data = {
            "wage": 3000,
            "position": "Chef d'équipe"
        }
        response = client.patch(f"/hr/contracts/{contract_id}", json=update_data)
        assert response.status_code == 200
        updated_contract = response.json()
        assert updated_contract["wage"] == 3000
        assert updated_contract["position"] == "Chef d'équipe"

        # 5. Terminer le contrat
        end_date = (date.today() + timedelta(days=30)).isoformat()
        response = client.post(f"/hr/contracts/{contract_id}/terminate", json={"end_date": end_date})
        assert response.status_code == 200
        terminated_contract = response.json()
        assert terminated_contract["is_active"] == False
        assert terminated_contract["end_date"] == end_date

    def test_contract_validations(self, client: TestClient, db: Session):
        """Test des validations des contrats"""
        # 1. Tentative de création avec un employé inexistant
        invalid_contract = {
            "employee_id": "invalid_id",
            "type": "CDI",
            "start_date": date.today().isoformat(),
            "wage": 2500,
            "position": "Agriculteur",
            "department": "Production"
        }
        response = client.post("/hr/contracts", json=invalid_contract)
        assert response.status_code == 400

        # 2. Tentative de création avec des données invalides
        employee = create_test_employee(db)
        invalid_data = {
            "employee_id": employee.id,
            "type": "INVALID_TYPE",
            "start_date": date.today().isoformat(),
            "wage": -1000,  # Salaire négatif
            "position": "",  # Position vide
            "department": "Production"
        }
        response = client.post("/hr/contracts", json=invalid_data)
        assert response.status_code == 422

        # 3. Tentative de mise à jour d'un contrat inexistant
        response = client.patch("/hr/contracts/invalid_id", json={"wage": 3000})
        assert response.status_code == 404

    def test_contract_queries(self, client: TestClient, db: Session):
        """Test des requêtes de contrats"""
        # 1. Créer des données de test
        employee = create_test_employee(db)
        contract = create_test_contract(db, employee.id)

        # 2. Tester la récupération des contrats actifs
        response = client.get("/hr/contracts/active")
        assert response.status_code == 200
        active_contracts = response.json()
        assert len(active_contracts) > 0
        assert any(c["id"] == contract.id for c in active_contracts)

        # 3. Tester la récupération des contrats d'un employé
        response = client.get(f"/hr/contracts/employee/{employee.id}")
        assert response.status_code == 200
        employee_contracts = response.json()
        assert len(employee_contracts) > 0
        assert employee_contracts[0]["employee_id"] == employee.id

        # 4. Tester la récupération des contrats expirants
        # Créer un contrat qui expire bientôt
        expiring_contract = Contract(
            id="expiring_contract_e2e",
            employee_id=employee.id,
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

        response = client.get("/hr/contracts/expiring/30")
        assert response.status_code == 200
        expiring_contracts = response.json()
        assert len(expiring_contracts) > 0
        assert any(c["id"] == expiring_contract.id for c in expiring_contracts)

    def test_multiple_contracts_handling(self, client: TestClient, db: Session):
        """Test de la gestion de plusieurs contrats pour un même employé"""
        # 1. Créer un employé
        employee = create_test_employee(db)

        # 2. Créer le premier contrat
        contract1_data = {
            "employee_id": employee.id,
            "type": "CDI",
            "start_date": date.today().isoformat(),
            "wage": 2500,
            "position": "Agriculteur",
            "department": "Production"
        }
        response = client.post("/hr/contracts", json=contract1_data)
        assert response.status_code == 201
        contract1_id = response.json()["id"]

        # 3. Créer un deuxième contrat pour le même employé
        contract2_data = {
            "employee_id": employee.id,
            "type": "CDI",
            "start_date": date.today().isoformat(),
            "wage": 3000,
            "position": "Chef d'équipe",
            "department": "Production"
        }
        response = client.post("/hr/contracts", json=contract2_data)
        assert response.status_code == 201

        # 4. Vérifier que le premier contrat est maintenant inactif
        response = client.get(f"/hr/contracts/{contract1_id}")
        assert response.status_code == 200
        contract1 = response.json()
        assert contract1["is_active"] == False
