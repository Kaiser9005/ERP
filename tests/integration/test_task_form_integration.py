import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.main import app
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskStatus, TaskPriority, TaskCategory

@pytest.fixture
def test_task_data():
    tomorrow = datetime.now() + timedelta(days=1)
    return {
        "title": "Tâche Test Intégration",
        "description": "Description de la tâche d'intégration",
        "status": TaskStatus.A_FAIRE,
        "priority": TaskPriority.MOYENNE,
        "category": TaskCategory.PRODUCTION,
        "start_date": datetime.now().date().isoformat(),
        "due_date": tomorrow.date().isoformat(),
        "project_id": 1,
        "weather_dependent": True,
        "min_temperature": 15,
        "max_temperature": 30,
        "max_wind_speed": 20,
        "max_precipitation": 5,
        "completion_percentage": 0,
        "resources": [],
        "dependencies": []
    }

@pytest.mark.integration
def test_create_task_integration(client: TestClient, db: Session, test_task_data):
    response = client.post("/api/v1/tasks/", json=test_task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == test_task_data["title"]
    assert data["weather_dependent"] == test_task_data["weather_dependent"]
    
    # Vérifier que la tâche est bien dans la base de données
    db_task = db.query(Task).filter(Task.id == data["id"]).first()
    assert db_task is not None
    assert db_task.title == test_task_data["title"]

@pytest.mark.integration
def test_update_task_integration(client: TestClient, db: Session, test_task_data):
    # Créer d'abord une tâche
    response = client.post("/api/v1/tasks/", json=test_task_data)
    task_id = response.json()["id"]
    
    # Modifier la tâche
    update_data = test_task_data.copy()
    update_data["title"] = "Tâche Modifiée"
    update_data["completion_percentage"] = 50
    
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Tâche Modifiée"
    assert data["completion_percentage"] == 50

@pytest.mark.integration
def test_task_weather_validation_integration(client: TestClient, test_task_data):
    # Tester la validation des champs météo
    invalid_data = test_task_data.copy()
    invalid_data["weather_dependent"] = True
    invalid_data["min_temperature"] = None
    
    response = client.post("/api/v1/tasks/", json=invalid_data)
    assert response.status_code == 422
    
    errors = response.json()["detail"]
    assert any("min_temperature" in error["loc"] for error in errors)

@pytest.mark.integration
def test_task_date_validation_integration(client: TestClient, test_task_data):
    # Tester la validation des dates
    invalid_data = test_task_data.copy()
    invalid_data["due_date"] = (datetime.now() - timedelta(days=1)).date().isoformat()
    
    response = client.post("/api/v1/tasks/", json=invalid_data)
    assert response.status_code == 422
    
    errors = response.json()["detail"]
    assert any("due_date" in error["loc"] for error in errors)

@pytest.mark.integration
def test_task_dependencies_integration(client: TestClient, db: Session, test_task_data):
    # Créer une première tâche
    response = client.post("/api/v1/tasks/", json=test_task_data)
    task1_id = response.json()["id"]
    
    # Créer une deuxième tâche dépendante de la première
    task2_data = test_task_data.copy()
    task2_data["title"] = "Tâche Dépendante"
    task2_data["dependencies"] = [{"dependent_on_id": task1_id, "dependency_type": "FINISH_TO_START"}]
    
    response = client.post("/api/v1/tasks/", json=task2_data)
    assert response.status_code == 201
    
    data = response.json()
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["dependent_on_id"] == task1_id

@pytest.mark.integration
def test_task_resources_integration(client: TestClient, db: Session, test_task_data):
    # Créer une tâche avec des ressources
    task_with_resources = test_task_data.copy()
    task_with_resources["resources"] = [
        {
            "resource_id": 1,
            "quantity_required": 10,
            "quantity_used": 0
        }
    ]
    
    response = client.post("/api/v1/tasks/", json=task_with_resources)
    assert response.status_code == 201
    
    data = response.json()
    assert len(data["resources"]) == 1
    assert data["resources"][0]["quantity_required"] == 10

@pytest.mark.integration
def test_task_completion_update_integration(client: TestClient, db: Session, test_task_data):
    # Créer une tâche
    response = client.post("/api/v1/tasks/", json=test_task_data)
    task_id = response.json()["id"]
    
    # Mettre à jour la progression
    update_data = {"completion_percentage": 75}
    response = client.patch(f"/api/v1/tasks/{task_id}/completion", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["completion_percentage"] == 75
    
    # Vérifier que le statut est mis à jour automatiquement
    assert data["status"] == TaskStatus.EN_COURS

@pytest.mark.integration
def test_task_weather_conditions_integration(client: TestClient, db: Session, test_task_data):
    # Créer une tâche dépendante de la météo
    response = client.post("/api/v1/tasks/", json=test_task_data)
    task_id = response.json()["id"]
    
    # Vérifier les conditions météo pour la tâche
    response = client.get(f"/api/v1/tasks/{task_id}/weather-conditions")
    assert response.status_code == 200
    
    data = response.json()
    assert "weather_suitable" in data
    assert "weather_conditions" in data
    assert "weather_warnings" in data
