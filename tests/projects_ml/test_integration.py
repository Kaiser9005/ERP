"""Tests d'intégration pour les modules ML des projets."""

import pytest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.projects_ml import ProjectsML

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def weather_service():
    """Fixture pour le service météo."""
    return AsyncMock(spec=WeatherService)

@pytest.fixture
def iot_service():
    """Fixture pour le service IoT."""
    return AsyncMock(spec=IoTService)

@pytest.fixture
def cache_service():
    """Fixture pour le service de cache."""
    return AsyncMock(spec=CacheService)

@pytest.fixture
def projects_ml(db_session, weather_service, iot_service, cache_service):
    """Fixture pour le service ML des projets."""
    service = ProjectsML(db_session)
    service._ml_service.weather_service = weather_service
    service._ml_service.iot_service = iot_service
    service._ml_service.cache = cache_service
    service._optimizer.cache = cache_service
    service._analyzer.iot_service = iot_service
    service._analyzer.cache = cache_service
    service._weather.weather_service = weather_service
    service._weather.iot_service = iot_service
    service._weather.cache = cache_service
    return service

@pytest.fixture
def sample_tasks():
    """Fixture pour les tâches exemple."""
    return [{
        "id": "T1",
        "name": "Tâche 1",
        "status": TaskStatus.IN_PROGRESS,
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=5),
        "progress": 50,
        "dependencies": [],
        "resources": ["R1"],
        "metrics": {"quality": 0.85},
        "weather_sensitive": True,
        "weather_conditions": ["TEMPERATURE", "RAIN"]
    }, {
        "id": "T2",
        "name": "Tâche 2",
        "status": TaskStatus.COMPLETED,
        "start_date": date.today() + timedelta(days=3),
        "end_date": date.today() + timedelta(days=8),
        "progress": 100,
        "dependencies": ["T1"],
        "resources": ["R2"],
        "metrics": {"quality": 0.95},
        "weather_sensitive": True,
        "weather_conditions": ["WIND", "FROST"]
    }]

@pytest.fixture
def sample_resources():
    """Fixture pour les ressources exemple."""
    return [{
        "id": "R1",
        "type": ResourceType.HUMAN,
        "name": "Resource 1",
        "availability": 0.8,
        "efficiency": 0.9,
        "cost": 1000.0
    }, {
        "id": "R2",
        "type": ResourceType.MATERIAL,
        "name": "Resource 2",
        "availability": 1.0,
        "efficiency": 0.95,
        "cost": 500.0
    }]

@pytest.fixture
def sample_weather():
    """Fixture pour les données météo exemple."""
    return {
        "daily": [{
            "date": date.today() + timedelta(days=i),
            "temperature": 22.5,
            "temperature_min": 15.0,
            "precipitation": 5.0,
            "wind_speed": 25.0
        } for i in range(10)]
    }

@pytest.fixture
def sample_iot_data():
    """Fixture pour les données IoT exemple."""
    return {
        SensorType.TEMPERATURE_SOL: {
            "readings": [
                {"timestamp": datetime.utcnow(), "value": 22.5}
            ],
            "stats": {
                "moyenne": 22.5,
                "minimum": 20.0,
                "maximum": 25.0
            },
            "health": {
                "status": SensorStatus.ACTIF,
                "battery_level": 85
            }
        },
        SensorType.HUMIDITE_SOL: {
            "readings": [
                {"timestamp": datetime.utcnow(), "value": 65.0}
            ],
            "stats": {
                "moyenne": 65.0,
                "minimum": 60.0,
                "maximum": 70.0
            },
            "health": {
                "status": SensorStatus.ACTIF,
                "battery_level": 90
            }
        }
    }

class TestProjectsMLIntegration:
    """Tests d'intégration pour ProjectsML."""

    async def test_predict_success_with_optimization(
        self,
        projects_ml,
        sample_tasks,
        sample_resources,
        sample_weather,
        sample_iot_data
    ):
        """Test de la prédiction avec optimisation."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        projects_ml._ml_service._get_project_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._ml_service._get_project_resources = AsyncMock(return_value=sample_resources)
        projects_ml._ml_service._get_iot_data = AsyncMock(return_value=sample_iot_data)
        projects_ml._optimizer._get_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._optimizer._get_resources = AsyncMock(return_value=sample_resources)
        
        # Exécution
        success = await projects_ml.predict_project_success(project_id)
        optimization = await projects_ml.optimize_resource_allocation(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "probability" in success
        assert "risk_factors" in success
        assert "recommendations" in success
        
        assert "optimal_allocation" in optimization
        assert "efficiency_score" in optimization
        assert "bottlenecks" in optimization
        assert "recommendations" in optimization
        
        # Vérification cohérence
        if success["probability"] < 0.5:
            assert any(
                "ressources" in r.lower()
                for r in success["recommendations"]
            )
            assert optimization["efficiency_score"] < 0.7

    async def test_performance_with_weather(
        self,
        projects_ml,
        sample_tasks,
        sample_resources,
        sample_weather,
        sample_iot_data
    ):
        """Test de l'analyse performance avec météo."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        projects_ml._analyzer._get_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._analyzer._get_resources = AsyncMock(return_value=sample_resources)
        projects_ml._analyzer._get_iot_data = AsyncMock(return_value=sample_iot_data)
        projects_ml._weather._get_weather_sensitive_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml.weather_service.get_forecast = AsyncMock(return_value=sample_weather)
        projects_ml._weather._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        performance = await projects_ml.analyze_performance(
            project_id,
            start_date,
            end_date
        )
        weather = await projects_ml.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "kpis" in performance
        assert "trends" in performance
        assert "predictions" in performance
        assert "recommendations" in performance
        
        assert "impact_score" in weather
        assert "affected_tasks" in weather
        assert "risk_periods" in weather
        assert "alternatives" in weather
        
        # Vérification cohérence
        if weather["impact_score"] > 0.7:
            assert performance["kpis"]["risk_score"] > 0.5
            assert any(
                "météo" in r.lower()
                for r in performance["recommendations"]
            )

    async def test_optimization_with_weather_constraints(
        self,
        projects_ml,
        sample_tasks,
        sample_resources,
        sample_weather,
        sample_iot_data
    ):
        """Test de l'optimisation avec contraintes météo."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        projects_ml._optimizer._get_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._optimizer._get_resources = AsyncMock(return_value=sample_resources)
        projects_ml._weather._get_weather_sensitive_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml.weather_service.get_forecast = AsyncMock(return_value=sample_weather)
        projects_ml._weather._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        weather = await projects_ml.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )
        optimization = await projects_ml.optimize_resource_allocation(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "alternatives" in weather
        assert "optimal_allocation" in optimization
        
        # Vérification cohérence
        if weather["alternatives"]:
            affected_tasks = {alt["task_id"] for alt in weather["alternatives"]}
            optimized_tasks = {
                alloc["task_id"]
                for alloc in optimization["optimal_allocation"]
            }
            
            # Les tâches affectées par la météo doivent être réallouées
            assert affected_tasks.intersection(optimized_tasks)

    async def test_performance_impact_on_success(
        self,
        projects_ml,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de l'impact performance sur le succès."""
        # Configuration
        project_id = "P1"
        
        projects_ml._ml_service._get_project_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._ml_service._get_project_resources = AsyncMock(return_value=sample_resources)
        projects_ml._ml_service._get_iot_data = AsyncMock(return_value=sample_iot_data)
        projects_ml._analyzer._get_tasks = AsyncMock(return_value=sample_tasks)
        projects_ml._analyzer._get_resources = AsyncMock(return_value=sample_resources)
        projects_ml._analyzer._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        performance = await projects_ml.analyze_performance(project_id)
        success = await projects_ml.predict_project_success(project_id)
        
        # Vérifications
        assert "kpis" in performance
        assert "probability" in success
        
        # Vérification cohérence
        if performance["kpis"]["schedule_performance"] < 0.5 or \
           performance["kpis"]["cost_performance"] < 0.5:
            assert success["probability"] < 0.7
            assert any(
                "performance" in r.lower()
                for r in success["recommendations"]
            )
