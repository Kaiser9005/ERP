"""Tests pour le service principal ML des projets."""

import pytest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, AsyncMock
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.projects_ml_service import ProjectMLService

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def ml_service(db_session):
    """Fixture pour le service ML."""
    return ProjectMLService(db_session)

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

class TestProjectMLService:
    """Tests pour ProjectMLService."""

    async def test_predict_project_success(
        self,
        ml_service,
        sample_tasks,
        sample_resources
    ):
        """Test de la prédiction de succès."""
        # Configuration
        project_id = "P1"
        ml_service.projects_ml.predict_project_success = AsyncMock(return_value={
            "probability": 0.8,
            "risk_factors": [],
            "recommendations": []
        })
        
        # Exécution
        result = await ml_service.predict_project_success(project_id)
        
        # Vérifications
        assert "probability" in result
        assert "risk_factors" in result
        assert "recommendations" in result
        ml_service.projects_ml.predict_project_success.assert_called_once_with(
            project_id,
            None
        )

    async def test_optimize_resource_allocation(
        self,
        ml_service,
        sample_tasks,
        sample_resources
    ):
        """Test de l'optimisation des ressources."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        ml_service.projects_ml.optimize_resource_allocation = AsyncMock(return_value={
            "optimal_allocation": [],
            "efficiency_score": 0.85,
            "bottlenecks": [],
            "recommendations": []
        })
        
        # Exécution
        result = await ml_service.optimize_resource_allocation(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "optimal_allocation" in result
        assert "efficiency_score" in result
        assert "bottlenecks" in result
        assert "recommendations" in result
        ml_service.projects_ml.optimize_resource_allocation.assert_called_once_with(
            project_id,
            start_date,
            end_date
        )

    async def test_analyze_project_performance(
        self,
        ml_service,
        sample_tasks,
        sample_resources
    ):
        """Test de l'analyse de performance."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        ml_service.projects_ml.analyze_performance = AsyncMock(return_value={
            "kpis": {},
            "trends": {},
            "predictions": {},
            "recommendations": []
        })
        
        # Exécution
        result = await ml_service.analyze_project_performance(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "kpis" in result
        assert "trends" in result
        assert "predictions" in result
        assert "recommendations" in result
        ml_service.projects_ml.analyze_performance.assert_called_once_with(
            project_id,
            start_date,
            end_date
        )

    async def test_predict_weather_impact(
        self,
        ml_service,
        sample_tasks
    ):
        """Test de la prédiction d'impact météo."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        ml_service.projects_ml.analyze_weather_impact = AsyncMock(return_value={
            "impact_score": 0.7,
            "affected_tasks": [],
            "risk_periods": [],
            "alternatives": []
        })
        
        # Exécution
        result = await ml_service.predict_weather_impact(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "impact_score" in result
        assert "affected_tasks" in result
        assert "risk_periods" in result
        assert "alternatives" in result
        ml_service.projects_ml.analyze_weather_impact.assert_called_once_with(
            project_id,
            start_date,
            end_date
        )

    async def test_error_handling(self, ml_service):
        """Test de la gestion des erreurs."""
        # Configuration
        project_id = "P1"
        ml_service.projects_ml.predict_project_success = AsyncMock(
            side_effect=Exception("Test error")
        )
        
        # Vérification
        with pytest.raises(Exception) as exc:
            await ml_service.predict_project_success(project_id)
        assert str(exc.value) == "Test error"
