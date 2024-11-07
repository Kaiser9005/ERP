import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import date, datetime
from ....models.production import Parcelle, CycleCulture, Recolte, ProductionEvent
from ....schemas.production import (
    ParcelleCreate, CycleCultureCreate, RecolteCreate, ProductionEventCreate
)

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

    response = client.post("/api/v1/production/parcelles/", json=parcelle_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == parcelle_data["code"]
    assert data["culture_type"] == parcelle_data["culture_type"]

def test_create_cycle_culture(client: TestClient, db_session):
    cycle_data = {
        "parcelle_id": str(uuid4()),
        "date_debut": str(date.today()),
        "rendement_prevu": 1200.5,
        "notes": "Test cycle"
    }

    response = client.post("/api/v1/production/cycles-culture/", json=cycle_data)
    assert response.status_code == 200
    data = response.json()
    assert data["parcelle_id"] == cycle_data["parcelle_id"]
    assert float(data["rendement_prevu"]) == cycle_data["rendement_prevu"]

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

    response = client.post("/api/v1/production/recoltes/", json=recolte_data)
    assert response.status_code == 200
    data = response.json()
    assert float(data["quantite_kg"]) == recolte_data["quantite_kg"]
    assert data["qualite"] == recolte_data["qualite"]

def test_create_production_event(client: TestClient, db_session):
    event_data = {
        "parcelle_id": str(uuid4()),
        "type": "MAINTENANCE",
        "date_debut": datetime.now().isoformat(),
        "description": "Test event",
        "responsable_id": str(uuid4())
    }

    response = client.post("/api/v1/production/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == event_data["type"]
    assert data["description"] == event_data["description"]

def test_get_production_stats(client: TestClient, db_session):
    response = client.get("/api/v1/production/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_surface" in data
    assert "parcelles_actives" in data
    assert "production_mensuelle" in data
    assert "rendement_moyen" in data

def test_filter_parcelles(client: TestClient, db_session):
    response = client.get("/api/v1/production/parcelles/?culture_type=PALMIER")
    assert response.status_code == 200
    data = response.json()
    assert all(p["culture_type"] == "PALMIER" for p in data)

def test_filter_recoltes_by_date(client: TestClient, db_session):
    today = date.today().isoformat()
    response = client.get(f"/api/v1/production/recoltes/?date_debut={today}")
    assert response.status_code == 200

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

@pytest.fixture
def sample_cycle_culture(db_session, sample_parcelle):
    cycle = CycleCulture(
        parcelle_id=sample_parcelle.id,
        date_debut=date.today(),
        rendement_prevu=1200.5
    )
    db_session.add(cycle)
    db_session.commit()
    return cycle

@pytest.fixture
def sample_recolte(db_session, sample_parcelle):
    recolte = Recolte(
        parcelle_id=sample_parcelle.id,
        date_recolte=datetime.now(),
        quantite_kg=500.5,
        qualite="A",
        conditions_meteo={
            "temperature": 25.5,
            "humidite": 75.0,
            "precipitation": 0.0
        }
    )
    db_session.add(recolte)
    db_session.commit()
    return recolte
