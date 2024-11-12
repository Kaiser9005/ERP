import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import HTTPException

from models.task import Task, TaskResource, TaskDependency
from models.resource import Resource, ResourceStatus
from services.task_service import TaskService
from services.weather_service import WeatherService
from schemas.task import TaskCreate, TaskFormData

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test"""
    # Création des ressources de test
    resource = Resource(
        name="Palmiers",
        type="MATERIEL",
        status=ResourceStatus.DISPONIBLE,
        quantity_total=100,
        quantity_available=100,
        quantity_reserved=0,
        unit="unités"
    )
    test_session.add(resource)
    test_session.commit()

    # Création d'une tâche de test
    task = Task(
        title="Tâche test",
        description="Description test",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        weather_dependent=True,
        min_temperature=20,
        max_temperature=35
    )
    test_session.add(task)
    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(TaskResource).delete()
    test_session.query(TaskDependency).delete()
    test_session.query(Task).delete()
    test_session.query(Resource).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_create_weather_dependent_task(test_db: Session, test_client: TestClient):
    """Test de création d'une tâche dépendante de la météo"""
    task_service = TaskService(test_db)
    weather_service = WeatherService()

    # Création de la tâche
    task_data = TaskFormData(
        title="Plantation zone B",
        description="Planter 50 palmiers",
        project_id=1,
        status="A_FAIRE",
        priority="HAUTE",
        category="PLANTATION",
        weather_dependent=True,
        min_temperature=20,
        max_temperature=35,
        max_wind_speed=20,
        max_precipitation=5,
        resources=[{
            "resource_id": 1,
            "quantity_required": 50,
            "quantity_used": 0
        }]
    )

    task = await task_service.create_task(task_data)
    assert task.weather_dependent == True
    assert task.min_temperature == 20
    assert task.max_temperature == 35

    # Vérification des conditions météo
    task_weather = await task_service.get_task_with_weather(task.id)
    assert "weather_suitable" in task_weather
    assert "weather_conditions" in task_weather
    assert "weather_warnings" in task_weather

    # Vérification de la réservation des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 50
    assert resource.quantity_reserved == 50

@pytest.mark.asyncio
async def test_task_resource_management(test_db: Session):
    """Test de la gestion des ressources d'une tâche"""
    task_service = TaskService(test_db)

    # Création d'une tâche avec ressources
    task_data = TaskFormData(
        title="Tâche avec ressources",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        resources=[{
            "resource_id": 1,
            "quantity_required": 30,
            "quantity_used": 0
        }]
    )

    task = await task_service.create_task(task_data)
    
    # Vérification de la réservation initiale
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 70
    assert resource.quantity_reserved == 30

    # Mise à jour de l'utilisation des ressources
    await task_service.update_task_resource(task.id, 1, 20)
    task_resource = test_db.query(TaskResource).first()
    assert task_resource.quantity_used == 20

    # Marquage de la tâche comme terminée
    task_update = TaskFormData(
        title=task.title,
        project_id=task.project_id,
        status="TERMINEE",
        priority=task.priority,
        category=task.category,
        completion_percentage=100
    )
    updated_task = await task_service.update_task(task.id, task_update)

    # Vérification de la libération des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE

@pytest.mark.asyncio
async def test_task_dependencies(test_db: Session):
    """Test de la gestion des dépendances entre tâches"""
    task_service = TaskService(test_db)

    # Création de deux tâches avec une dépendance
    task1_data = TaskFormData(
        title="Tâche 1",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION"
    )
    task1 = await task_service.create_task(task1_data)

    task2_data = TaskFormData(
        title="Tâche 2",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        dependencies=[{
            "dependent_on_id": task1.id,
            "dependency_type": "finish_to_start"
        }]
    )
    task2 = await task_service.create_task(task2_data)

    # Vérification de la dépendance
    dependencies = test_db.query(TaskDependency).all()
    assert len(dependencies) == 1
    assert dependencies[0].task_id == task2.id
    assert dependencies[0].dependent_on_id == task1.id

    # Vérification de la détection des dépendances circulaires
    task3_data = TaskFormData(
        title="Tâche 3",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        dependencies=[{
            "dependent_on_id": task2.id,
            "dependency_type": "finish_to_start"
        }]
    )
    task3 = await task_service.create_task(task3_data)

    # Tentative de création d'une dépendance circulaire
    with pytest.raises(HTTPException) as exc_info:
        task1_update = TaskFormData(
            title=task1.title,
            project_id=task1.project_id,
            status=task1.status,
            priority=task1.priority,
            category=task1.category,
            dependencies=[{
                "dependent_on_id": task3.id,
                "dependency_type": "finish_to_start"
            }]
        )
        await task_service.update_task(task1.id, task1_update)

    assert exc_info.value.status_code == 400
    assert "dépendance circulaire" in str(exc_info.value.detail).lower()

@pytest.mark.asyncio
async def test_weather_dependent_tasks_list(test_db: Session):
    """Test de la récupération des tâches dépendantes de la météo"""
    task_service = TaskService(test_db)

    # Création de tâches avec et sans dépendance météo
    weather_task = TaskFormData(
        title="Tâche météo",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        weather_dependent=True,
        min_temperature=20,
        max_temperature=35
    )
    await task_service.create_task(weather_task)

    normal_task = TaskFormData(
        title="Tâche normale",
        project_id=1,
        status="A_FAIRE",
        priority="MOYENNE",
        category="PLANTATION",
        weather_dependent=False
    )
    await task_service.create_task(normal_task)

    # Récupération des tâches météo-dépendantes
    weather_tasks = await task_service.get_weather_dependent_tasks()
    
    assert len(weather_tasks) == 1
    assert weather_tasks[0].title == "Tâche météo"
    assert "weather_suitable" in weather_tasks[0]
    assert "weather_conditions" in weather_tasks[0]
    assert "weather_warnings" in weather_tasks[0]

@pytest.mark.asyncio
async def test_task_completion_workflow(test_db: Session):
    """Test du workflow complet de réalisation d'une tâche"""
    task_service = TaskService(test_db)

    # Création d'une tâche avec ressources
    task_data = TaskFormData(
        title="Tâche workflow",
        project_id=1,
        status="A_FAIRE",
        priority="HAUTE",
        category="PLANTATION",
        weather_dependent=True,
        min_temperature=20,
        max_temperature=35,
        resources=[{
            "resource_id": 1,
            "quantity_required": 40,
            "quantity_used": 0
        }]
    )

    # Création
    task = await task_service.create_task(task_data)
    assert task.status == "A_FAIRE"
    assert task.completion_percentage == 0

    # Mise en cours
    task_update = TaskFormData(
        title=task.title,
        project_id=task.project_id,
        status="EN_COURS",
        priority=task.priority,
        category=task.category,
        completion_percentage=30
    )
    task = await task_service.update_task(task.id, task_update)
    assert task.status == "EN_COURS"
    assert task.completion_percentage == 30

    # Utilisation des ressources
    await task_service.update_task_resource(task.id, 1, 20)
    resource = test_db.query(Resource).first()
    assert resource.quantity_reserved == 40
    assert resource.quantity_available == 60

    # Vérification météo
    task_weather = await task_service.get_task_with_weather(task.id)
    assert "weather_suitable" in task_weather

    # Finalisation
    task_update = TaskFormData(
        title=task.title,
        project_id=task.project_id,
        status="TERMINEE",
        priority=task.priority,
        category=task.category,
        completion_percentage=100
    )
    task = await task_service.update_task(task.id, task_update)
    assert task.status == "TERMINEE"
    assert task.completion_percentage == 100
    assert task.completed_date is not None

    # Vérification finale des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE
