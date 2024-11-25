"""
Tests d'intégration pour le service ML des projets
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
import asyncio

from services.projects_ml_service import ProjectsMLService
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType

@pytest.fixture
def ml_service_with_mocks(db_session):
    """Service ML avec mocks pour les dépendances"""
    service = ProjectsMLService(db_session)
    service.weather_service = MagicMock(spec=WeatherService)
    service.iot_service = MagicMock(spec=IoTService)
    service.cache = MagicMock(spec=CacheService)
    return service

@pytest.fixture
def weather_data():
    """Données météo de test"""
    return {
        "temperature": 20,
        "precipitation": 0,
        "humidity": 65,
        "wind_speed": 10,
        "forecast": [
            {
                "date": date.today() + timedelta(days=i),
                "temperature": 20 + i,
                "precipitation": i * 2
            }
            for i in range(7)
        ]
    }

@pytest.fixture
def iot_data():
    """Données IoT de test"""
    return {
        "sensors": [
            {
                "id": f"S{i}",
                "type": "SOIL_MOISTURE",
                "value": 35 + i,
                "timestamp": datetime.now() - timedelta(hours=i)
            }
            for i in range(5)
        ]
    }

async def test_weather_integration(ml_service_with_mocks, project, weather_data):
    """Test de l'intégration avec le service météo"""
    # Configuration mock météo
    ml_service_with_mocks.weather_service.get_forecast.return_value = weather_data
    
    # Prédiction impact
    impact = await ml_service_with_mocks.predict_weather_impact(
        project_id=project.id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7)
    )
    
    # Vérifications
    assert ml_service_with_mocks.weather_service.get_forecast.called
    assert "impact_score" in impact
    assert "affected_tasks" in impact
    assert "risk_periods" in impact
    assert "alternatives" in impact

async def test_iot_integration(ml_service_with_mocks, project, iot_data):
    """Test de l'intégration avec le service IoT"""
    # Configuration mock IoT
    ml_service_with_mocks.iot_service.get_period_data.return_value = iot_data
    
    # Analyse performance
    performance = await ml_service_with_mocks.analyze_project_performance(
        project_id=project.id,
        start_date=date.today() - timedelta(days=7),
        end_date=date.today()
    )
    
    # Vérifications
    assert ml_service_with_mocks.iot_service.get_period_data.called
    assert "kpis" in performance
    assert "trends" in performance
    assert "predictions" in performance

async def test_cache_integration(ml_service_with_mocks, project):
    """Test de l'intégration avec le cache"""
    # Premier appel - pas de cache
    ml_service_with_mocks.cache.get.return_value = None
    prediction1 = await ml_service_with_mocks.predict_project_success(
        project_id=project.id
    )
    
    # Deuxième appel - utilise le cache
    ml_service_with_mocks.cache.get.return_value = prediction1
    prediction2 = await ml_service_with_mocks.predict_project_success(
        project_id=project.id
    )
    
    # Vérifications
    assert ml_service_with_mocks.cache.get.call_count == 2
    assert ml_service_with_mocks.cache.set.called
    assert prediction1 == prediction2

async def test_error_handling(ml_service_with_mocks, project):
    """Test de la gestion des erreurs"""
    # Configuration erreurs
    ml_service_with_mocks.weather_service.get_forecast.side_effect = Exception("Erreur météo")
    ml_service_with_mocks.iot_service.get_period_data.side_effect = Exception("Erreur IoT")
    ml_service_with_mocks.cache.get.side_effect = Exception("Erreur cache")
    
    # Exécution avec erreurs
    impact = await ml_service_with_mocks.predict_weather_impact(
        project_id=project.id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7)
    )
    
    # Vérifications
    assert "impact_score" in impact  # Valeurs par défaut
    assert "affected_tasks" in impact
    assert "risk_periods" in impact
    assert "alternatives" in impact
    assert impact.get("error_handled")

async def test_timeout_handling(ml_service_with_mocks, project):
    """Test de la gestion des timeouts"""
    # Configuration délais
    async def delayed_weather():
        await asyncio.sleep(2)
        return {}
        
    ml_service_with_mocks.weather_service.get_forecast.side_effect = delayed_weather
    
    # Exécution avec timeout
    async with asyncio.timeout(1):
        impact = await ml_service_with_mocks.predict_weather_impact(
            project_id=project.id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )
    
    # Vérifications
    assert "impact_score" in impact  # Valeurs par défaut
    assert impact.get("timeout_handled")

async def test_invalid_data_handling(ml_service_with_mocks, project):
    """Test de la gestion des données invalides"""
    # Configuration données invalides
    ml_service_with_mocks.weather_service.get_forecast.return_value = {
        "temperature": "invalid",
        "precipitation": None
    }
    
    ml_service_with_mocks.iot_service.get_period_data.return_value = {
        "sensors": [{"value": "invalid"}]
    }
    
    # Exécution avec données invalides
    performance = await ml_service_with_mocks.analyze_project_performance(
        project_id=project.id,
        start_date=date.today() - timedelta(days=7),
        end_date=date.today()
    )
    
    # Vérifications
    assert "kpis" in performance  # Valeurs par défaut
    assert "trends" in performance
    assert "predictions" in performance
    assert performance.get("data_validation_errors")

async def test_concurrent_access(ml_service_with_mocks, project):
    """Test des accès concurrents"""
    # Configuration délais variables
    async def delayed_response(delay):
        await asyncio.sleep(delay)
        return {"data": f"response after {delay}s"}
    
    ml_service_with_mocks.weather_service.get_forecast.side_effect = \
        lambda *args: delayed_response(0.1)
    ml_service_with_mocks.iot_service.get_period_data.side_effect = \
        lambda *args: delayed_response(0.2)
    
    # Exécution concurrente
    async def concurrent_request():
        return await ml_service_with_mocks.predict_weather_impact(
            project_id=project.id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )
    
    # Lancement de 5 requêtes simultanées
    results = await asyncio.gather(*[concurrent_request() for _ in range(5)])
    
    # Vérifications
    assert len(results) == 5
    assert all("impact_score" in r for r in results)

async def test_performance(ml_service_with_mocks, project):
    """Test des performances"""
    # Configuration données volumineuses
    weather_data = {
        "forecast": [
            {
                "date": date.today() + timedelta(days=i),
                "temperature": 20 + i,
                "precipitation": i * 2,
                "details": "x" * 1000  # 1KB de données par prévision
            }
            for i in range(365)  # Un an de prévisions
        ]
    }
    
    iot_data = {
        "sensors": [
            {
                "id": f"S{i}",
                "type": "SOIL_MOISTURE",
                "value": 35 + i,
                "timestamp": datetime.now() - timedelta(hours=i),
                "details": "x" * 1000  # 1KB de données par mesure
            }
            for i in range(1000)  # 1000 mesures
        ]
    }
    
    ml_service_with_mocks.weather_service.get_forecast.return_value = weather_data
    ml_service_with_mocks.iot_service.get_period_data.return_value = iot_data
    
    # Mesure temps d'exécution
    start_time = datetime.now()
    
    impact = await ml_service_with_mocks.predict_weather_impact(
        project_id=project.id,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=365)
    )
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    # Vérifications
    assert execution_time < 1.0  # Maximum 1 seconde
    assert "impact_score" in impact
    assert "affected_tasks" in impact
    assert "risk_periods" in impact
    assert "alternatives" in impact

async def test_ml_model_integration(ml_service_with_mocks, project):
    """Test de l'intégration des modèles ML"""
    # Prédiction avec différents modèles
    predictions = []
    for model in ["basic", "advanced", "ensemble"]:
        prediction = await ml_service_with_mocks.predict_project_success(
            project_id=project.id,
            ml_config={"model": model}
        )
        predictions.append(prediction)
    
    # Vérifications
    assert len(predictions) == 3
    assert all("success_probability" in p for p in predictions)
    assert all("risk_factors" in p for p in predictions)
    assert all("recommendations" in p for p in predictions)
    
    # Vérification cohérence
    probabilities = [p["success_probability"] for p in predictions]
    assert max(probabilities) - min(probabilities) < 0.2  # Max 20% d'écart

async def test_data_consistency(ml_service_with_mocks, project):
    """Test de la cohérence des données"""
    # Prédictions successives
    prediction1 = await ml_service_with_mocks.predict_project_success(
        project_id=project.id
    )
    
    # Modification projet
    task = Task(
        project_id=project.id,
        name="New Task",
        status=TaskStatus.IN_PROGRESS
    )
    ml_service_with_mocks.db.add(task)
    ml_service_with_mocks.db.commit()
    
    prediction2 = await ml_service_with_mocks.predict_project_success(
        project_id=project.id
    )
    
    # Vérifications
    assert prediction1["success_probability"] != prediction2["success_probability"]
    assert len(prediction2["risk_factors"]) >= len(prediction1["risk_factors"])
