import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException

from services.tache_service import TacheService
from models.tache import Tache, RessourceTache, CommentaireTache, DependanceTache, StatutTache, CategorieTache
from models.resource import Resource, ResourceStatus
from schemas.tache import TacheCreate, TacheUpdate, RessourceTacheCreate, CommentaireTacheCreate


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
def tache_service(mock_db):
    """Fixture pour le service de tâches"""
    return TacheService(mock_db)


@pytest.mark.asyncio
async def test_create_task(tache_service, mock_db):
    """Test de création d'une tâche simple"""
    # Préparation des données
    tache_data = TacheCreate(
        titre="Test Tâche",
        description="Test Description",
        projet_id=1,
        categorie=CategorieTache.PLANTATION,
        date_debut=datetime.now(),
        date_fin_prevue=datetime.now() + timedelta(days=1)
    )

    # Configuration du mock
    mock_tache = Mock(id=1)
    mock_db.add.return_value = None
    mock_db.flush.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    # Exécution
    result = await tache_service.create_task(tache_data)

    # Vérifications
    assert mock_db.add.called
    assert mock_db.commit.called
    assert result is not None


@pytest.mark.asyncio
async def test_create_task_with_resources(tache_service, mock_db):
    """Test de création d'une tâche avec ressources"""
    # Préparation des données
    resource = Mock(
        id=1,
        name="Test Resource",
        quantity_available=100,
        status=ResourceStatus.DISPONIBLE
    )
    mock_db.query(Resource).get.return_value = resource

    tache_data = TacheCreate(
        titre="Test Tâche",
        projet_id=1,
        ressources=[
            RessourceTacheCreate(
                ressource_id=1,
                quantite_requise=50
            )
        ]
    )

    # Exécution
    result = await tache_service.create_task(tache_data)

    # Vérifications
    assert mock_db.add.called
    assert resource.quantity_available == 50
    assert resource.quantity_reserved == 50


@pytest.mark.asyncio
async def test_create_task_insufficient_resources(tache_service, mock_db):
    """Test de création d'une tâche avec ressources insuffisantes"""
    # Préparation
    resource = Mock(
        id=1,
        name="Test Resource",
        quantity_available=30
    )
    mock_db.query(Resource).get.return_value = resource

    tache_data = TacheCreate(
        titre="Test Tâche",
        projet_id=1,
        ressources=[
            RessourceTacheCreate(
                ressource_id=1,
                quantite_requise=50
            )
        ]
    )

    # Vérification que l'exception est levée
    with pytest.raises(HTTPException) as exc_info:
        await tache_service.create_task(tache_data)
    assert exc_info.value.status_code == 400
    assert "Quantité insuffisante" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_task_with_weather(tache_service, mock_db, mock_weather_data):
    """Test de récupération d'une tâche avec données météo"""
    # Préparation
    tache = Mock(
        id=1,
        dependant_meteo=True,
        min_temperature=20,
        max_temperature=30,
        max_wind_speed=20,
        max_precipitation=5
    )
    mock_db.query(Tache).get.return_value = tache

    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_data):
        # Exécution
        result = await tache_service.get_task_with_weather(1)

        # Vérifications
        assert result.conditions_favorables is True
        assert result.conditions_meteo == mock_weather_data["current_conditions"]
        assert len(result.alertes_meteo) == 0


def test_update_task_completion(tache_service, mock_db):
    """Test de mise à jour d'une tâche terminée"""
    # Préparation
    tache = Mock(
        id=1,
        statut=StatutTache.EN_COURS
    )
    mock_db.query(Tache).get.return_value = tache

    ressource_tache = Mock(
        tache_id=1,
        ressource_id=1,
        quantite_requise=50
    )
    mock_db.query(RessourceTache).filter.return_value.all.return_value = [ressource_tache]

    resource = Mock(
        id=1,
        quantity_available=50,
        quantity_reserved=50
    )
    mock_db.query(Resource).get.return_value = resource

    update_data = TacheUpdate(
        statut=StatutTache.TERMINEE
    )

    # Exécution
    result = tache_service.update_task(1, update_data)

    # Vérifications
    assert result.statut == StatutTache.TERMINEE
    assert result.pourcentage_completion == 100
    assert result.date_fin_reelle is not None
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE


def test_delete_task(tache_service, mock_db):
    """Test de suppression d'une tâche"""
    # Préparation
    tache = Mock(id=1)
    ressource_tache = Mock(
        tache_id=1,
        ressource_id=1,
        quantite_requise=50
    )
    resource = Mock(
        id=1,
        quantity_available=50,
        quantity_reserved=50
    )

    mock_db.query(Tache).get.return_value = tache
    mock_db.query(RessourceTache).filter.return_value.all.return_value = [ressource_tache]
    mock_db.query(Resource).get.return_value = resource

    # Exécution
    tache_service.delete_task(1)

    # Vérifications
    assert mock_db.delete.called
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE


@pytest.mark.asyncio
async def test_get_weather_dependent_tasks(tache_service, mock_db, mock_weather_data):
    """Test de récupération des tâches dépendantes de la météo"""
    # Préparation
    taches = [
        Mock(
            id=1,
            dependant_meteo=True,
            min_temperature=20,
            max_temperature=30,
            statut=StatutTache.EN_COURS
        ),
        Mock(
            id=2,
            dependant_meteo=True,
            min_temperature=15,
            max_temperature=25,
            statut=StatutTache.A_FAIRE
        )
    ]
    mock_db.query(Tache).filter.return_value.all.return_value = taches

    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_data):
        # Exécution
        results = await tache_service.get_weather_dependent_tasks()

        # Vérifications
        assert len(results) == 2
        assert all(hasattr(tache, 'conditions_favorables') for tache in results)
        assert all(hasattr(tache, 'conditions_meteo') for tache in results)
        assert all(hasattr(tache, 'alertes_meteo') for tache in results)


def test_check_circular_dependency(tache_service, mock_db):
    """Test de détection des dépendances circulaires"""
    # Préparation des dépendances
    dependances = [
        Mock(tache_id=2, dependance_id=3),
        Mock(tache_id=3, dependance_id=1)
    ]
    mock_db.query(DependanceTache).filter.return_value.all.return_value = dependances

    # Test avec dépendance circulaire
    assert tache_service.check_circular_dependency(1, 2) is True

    # Test sans dépendance circulaire
    dependances = [Mock(tache_id=2, dependance_id=3)]
    mock_db.query(DependanceTache).filter.return_value.all.return_value = dependances
    assert tache_service.check_circular_dependency(1, 2) is False

def test_get_task(tache_service, mock_db):
    """Test de récupération d'une tâche"""
    # Préparation
    tache = Mock(id=1)
    mock_db.query(Tache).get.return_value = tache

    # Test récupération réussie
    result = tache_service.get_task(1)
    assert result == tache

    # Test tâche non trouvée
    mock_db.query(Tache).get.return_value = None
    with pytest.raises(HTTPException, match="Tâche non trouvée"):
        tache_service.get_task(999)

def test_get_tasks_by_project(tache_service, mock_db):
    """Test de récupération des tâches d'un projet"""
    # Préparation
    taches = [Mock(id=i) for i in range(1, 4)]
    query = mock_db.query(Tache)
    query.filter.return_value = query
    query.count.return_value = 3
    query.offset.return_value = query
    query.limit.return_value.all.return_value = taches

    # Test sans filtres
    result = tache_service.get_tasks_by_project(1)
    assert len(result["taches"]) == 3
    assert result["total"] == 3
    assert result["page"] == 1
    assert result["total_pages"] == 1

    # Test avec filtres
    result = tache_service.get_tasks_by_project(
        1,
        status=StatutTache.EN_COURS,
        category="PLANTATION"
    )
    assert len(result["taches"]) == 3
    assert query.filter.call_count >= 3  # Projet + status + category

def test_add_task_comment(tache_service, mock_db):
    """Test d'ajout d'un commentaire"""
    # Préparation
    tache = Mock(id=1)
    mock_db.query(Tache).get.return_value = tache
    
    comment_data = CommentaireTacheCreate(
        tache_id=1,
        utilisateur_id="user1",
        contenu="Test commentaire"
    )

    # Test ajout réussi
    result = tache_service.add_task_comment(comment_data)
    assert mock_db.add.called
    assert mock_db.commit.called

    # Test tâche non trouvée
    mock_db.query(Tache).get.return_value = None
    with pytest.raises(HTTPException, match="Tâche non trouvée"):
        tache_service.add_task_comment(comment_data)

def test_update_task_resource(tache_service, mock_db):
    """Test de mise à jour des ressources d'une tâche"""
    # Préparation
    task_resource = Mock(
        tache_id=1,
        ressource_id=1,
        quantite_requise=100
    )
    mock_db.query(RessourceTache).filter.return_value.first.return_value = task_resource

    # Test mise à jour réussie
    result = tache_service.update_task_resource(1, 1, 50)
    assert result.quantite_utilisee == 50
    assert mock_db.commit.called

    # Test quantité dépassée
    with pytest.raises(HTTPException, match="La quantité utilisée ne peut pas dépasser"):
        tache_service.update_task_resource(1, 1, 150)

    # Test ressource non trouvée
    mock_db.query(RessourceTache).filter.return_value.first.return_value = None
    with pytest.raises(HTTPException, match="Association tâche-ressource non trouvée"):
        tache_service.update_task_resource(1, 1, 50)

def test_get_dependent_tasks(tache_service, mock_db):
    """Test de récupération des tâches dépendantes"""
    # Préparation
    tache1 = Mock(id=1)
    tache2 = Mock(id=2)
    dependances = [
        Mock(tache=tache1),
        Mock(tache=tache2)
    ]
    mock_db.query(DependanceTache).filter.return_value.all.return_value = dependances

    # Test récupération
    result = tache_service.get_dependent_tasks(1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2