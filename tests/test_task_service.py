import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException

from services.task_service import TaskService
from models.task import Task, TaskResource, TaskComment, TaskDependency, TaskStatus, TaskCategory
from models.resource import Resource, ResourceStatus
from schemas.task import TaskCreate, TaskUpdate, TaskResourceCreate


@pytest.fixture
def mock_db():
    """Fixture pour simuler la base de données"""
    return Mock(spec=Session)


@pytest.fixture
def mock_weather_data():
    """Fixture pour simuler les données météo"""
    return {
        "current_conditions": {
            "temperature": 25,
            "humidity": 70,
            "precipitation": 0,
            "wind_speed": 15,
            "conditions": "Ensoleillé",
            "uv_index": 6,
            "cloud_cover": 30
        },
        "risks": {
            "precipitation": {"level": "LOW"},
            "temperature": {"level": "MEDIUM"}
        },
        "recommendations": []
    }


@pytest.fixture
def task_service(mock_db):
    """Fixture pour le service de tâches"""
    return TaskService(mock_db)


@pytest.mark.asyncio
async def test_create_task(task_service, mock_db):
    """Test de création d'une tâche simple"""
    # Préparation des données
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        project_id=1,
        category=TaskCategory.PLANTATION,
        start_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=1)
    )

    # Configuration du mock
    mock_task = Mock(id=1)
    mock_db.add.return_value = None
    mock_db.flush.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    # Exécution
    result = await task_service.create_task(task_data)

    # Vérifications
    assert mock_db.add.called
    assert mock_db.commit.called
    assert result is not None


@pytest.mark.asyncio
async def test_create_task_with_resources(task_service, mock_db):
    """Test de création d'une tâche avec ressources"""
    # Préparation des données
    resource = Mock(
        id=1,
        name="Test Resource",
        quantity_available=100,
        status=ResourceStatus.DISPONIBLE
    )
    mock_db.query(Resource).get.return_value = resource

    task_data = TaskCreate(
        title="Test Task",
        project_id=1,
        resources=[
            TaskResourceCreate(
                resource_id=1,
                quantity_required=50
            )
        ]
    )

    # Exécution
    result = await task_service.create_task(task_data)

    # Vérifications
    assert mock_db.add.called
    assert resource.quantity_available == 50
    assert resource.quantity_reserved == 50


@pytest.mark.asyncio
async def test_create_task_insufficient_resources(task_service, mock_db):
    """Test de création d'une tâche avec ressources insuffisantes"""
    # Préparation
    resource = Mock(
        id=1,
        name="Test Resource",
        quantity_available=30
    )
    mock_db.query(Resource).get.return_value = resource

    task_data = TaskCreate(
        title="Test Task",
        project_id=1,
        resources=[
            TaskResourceCreate(
                resource_id=1,
                quantity_required=50
            )
        ]
    )

    # Vérification que l'exception est levée
    with pytest.raises(HTTPException) as exc_info:
        await task_service.create_task(task_data)
    assert exc_info.value.status_code == 400
    assert "Quantité insuffisante" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_task_with_weather(task_service, mock_db, mock_weather_data):
    """Test de récupération d'une tâche avec données météo"""
    # Préparation
    task = Mock(
        id=1,
        weather_dependent=True,
        min_temperature=20,
        max_temperature=30,
        max_wind_speed=20,
        max_precipitation=5
    )
    mock_db.query(Task).get.return_value = task

    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_data):
        # Exécution
        result = await task_service.get_task_with_weather(1)

        # Vérifications
        assert result.weather_suitable is True
        assert result.weather_conditions == mock_weather_data["current_conditions"]
        assert len(result.weather_warnings) == 0


def test_update_task_completion(task_service, mock_db):
    """Test de mise à jour d'une tâche terminée"""
    # Préparation
    task = Mock(
        id=1,
        status=TaskStatus.EN_COURS
    )
    mock_db.query(Task).get.return_value = task

    task_resource = Mock(
        task_id=1,
        resource_id=1,
        quantity_required=50
    )
    mock_db.query(TaskResource).filter.return_value.all.return_value = [task_resource]

    resource = Mock(
        id=1,
        quantity_available=50,
        quantity_reserved=50
    )
    mock_db.query(Resource).get.return_value = resource

    update_data = TaskUpdate(
        status=TaskStatus.TERMINEE
    )

    # Exécution
    result = task_service.update_task(1, update_data)

    # Vérifications
    assert result.status == TaskStatus.TERMINEE
    assert result.completion_percentage == 100
    assert result.completed_date is not None
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE


def test_delete_task(task_service, mock_db):
    """Test de suppression d'une tâche"""
    # Préparation
    task = Mock(id=1)
    task_resource = Mock(
        task_id=1,
        resource_id=1,
        quantity_required=50
    )
    resource = Mock(
        id=1,
        quantity_available=50,
        quantity_reserved=50
    )

    mock_db.query(Task).get.return_value = task
    mock_db.query(TaskResource).filter.return_value.all.return_value = [task_resource]
    mock_db.query(Resource).get.return_value = resource

    # Exécution
    task_service.delete_task(1)

    # Vérifications
    assert mock_db.delete.called
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE


@pytest.mark.asyncio
async def test_get_weather_dependent_tasks(task_service, mock_db, mock_weather_data):
    """Test de récupération des tâches dépendantes de la météo"""
    # Préparation
    tasks = [
        Mock(
            id=1,
            weather_dependent=True,
            min_temperature=20,
            max_temperature=30,
            status=TaskStatus.EN_COURS
        ),
        Mock(
            id=2,
            weather_dependent=True,
            min_temperature=15,
            max_temperature=25,
            status=TaskStatus.A_FAIRE
        )
    ]
    mock_db.query(Task).filter.return_value.all.return_value = tasks

    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_data):
        # Exécution
        results = await task_service.get_weather_dependent_tasks()

        # Vérifications
        assert len(results) == 2
        assert all(hasattr(task, 'weather_suitable') for task in results)
        assert all(hasattr(task, 'weather_conditions') for task in results)
        assert all(hasattr(task, 'weather_warnings') for task in results)


def test_check_circular_dependency(task_service, mock_db):
    """Test de détection des dépendances circulaires"""
    # Préparation des dépendances
    dependencies = [
        Mock(task_id=2, dependent_on_id=3),
        Mock(task_id=3, dependent_on_id=1)
    ]
    mock_db.query(TaskDependency).filter.return_value.all.return_value = dependencies

    # Test avec dépendance circulaire
    assert task_service.check_circular_dependency(1, 2) is True

    # Test sans dépendance circulaire
    dependencies = [Mock(task_id=2, dependent_on_id=3)]
    mock_db.query(TaskDependency).filter.return_value.all.return_value = dependencies
    assert task_service.check_circular_dependency(1, 2) is False
