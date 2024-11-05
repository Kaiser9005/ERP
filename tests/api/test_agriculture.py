import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import date, datetime
from ....models.agriculture.parcelle import Parcelle, CycleCulture, Recolte
from ....schemas.agriculture import ParcelleCreate, CycleCultureCreate, RecolteCreate

def test_create_parcelle(client: TestClient, db_session):
    parcelle_data = {
        "code": "TEST001",
        "culture_type": "PALMIER",
        "surface_hectares": 5.5,
        "date_plantation": str(date.today()),
        "coordonnees_gps": {
            "latitude": 4.0511,
            "longitude": 9.7679
        },
        "responsable_id": str(uuid4()),
        "metadata": {"sol_type": "argileux"}
    }

    response = client.post("/api/v1/agriculture/parcelles/", json=parcelle_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == parcelle_data["code"]
    assert data["culture_type"] == parcelle_data["culture_type"]

def test_list_parcelles(client: TestClient, db_session):
    response = client.get("/api/v1/agriculture/parcelles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_cycle_culture(client: TestClient, db_session):
    # Créer d'abord une parcelle
    parcelle_id = str(uuid4())
    cycle_data = {
        "parcelle_id": parcelle_id,
        "date_debut": str(date.today()),
        "rendement_prevu": 1200.5,
        "notes": "Test cycle"
    }

    response = client.post("/api/v1/agriculture/cycles-culture/", json=cycle_data)
    assert response.status_code == 200
    data = response.json()
    assert data["parcelle_id"] == parcelle_id

def test_create_recolte(client: TestClient, db_session):
    recolte_data = {
        "parcelle_id": str(uuid4()),
        "date_recolte": datetime.now().isoformat(),
        "quantite_kg": 500.5,
        "qualite": "A",
        "conditions_meteo": {
            "temperature": 25.5,
            "humidite": 75.0,
            "precipitation": 0.0
        },
        "equipe_recolte": [str(uuid4()) for _ in range(3)],
        "notes": "Test récolte"
    }

    response = client.post("/api/v1/agriculture/recoltes/", json=recolte_data)
    assert response.status_code == 200
    data = response.json()
    assert data["quantite_kg"] == recolte_data["quantite_kg"]
    assert data["qualite"] == recolte_data["qualite"]

def test_filter_parcelles(client: TestClient, db_session):
    response = client.get("/api/v1/agriculture/parcelles/?culture_type=PALMIER")
    assert response.status_code == 200
    data = response.json()
    assert all(p["culture_type"] == "PALMIER" for p in data)

def test_update_parcelle(client: TestClient, db_session):
    parcelle_id = str(uuid4())
    update_data = {
        "statut": "EN_REPOS",
        "metadata": {"derniere_maintenance": str(date.today())}
    }

    response = client.put(f"/api/v1/agriculture/parcelles/{parcelle_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["statut"] == update_data["statut"]

def test_get_recolte_details(client: TestClient, db_session):
    recolte_id = str(uuid4())
    response = client.get(f"/api/v1/agriculture/recoltes/{recolte_id}")
    assert response.status_code in [200, 404]  # 404 si la récolte n'existe pas

@pytest.fixture
def sample_parcelle(db_session):
    parcelle = Parcelle(
        code="TEST001",
        culture_type="PALMIER",
        surface_hectares=5.5,
        date_plantation=date.today(),
        coordonnees_gps={"latitude": 4.0511, "longitude": 9.7679},
        responsable_id=uuid4()
    )
    db_session.add(parcelle)
    db_session.commit()
    return parcelle
