"""Tests pour l'analyse de performance."""

import pytest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.projects_ml.analysis import PerformanceAnalyzer

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def iot_service():
    """Fixture pour le service IoT."""
    return AsyncMock(spec=IoTService)

@pytest.fixture
def cache_service():
    """Fixture pour le service de cache."""
    return AsyncMock(spec=CacheService)

@pytest.fixture
def analyzer(db_session, iot_service, cache_service):
    """Fixture pour l'analyseur."""
    service = PerformanceAnalyzer(db_session)
    service.iot_service = iot_service
    service.cache = cache_service
    return service

@pytest.fixture
def sample_tasks():
    """Fixture pour les tâches exemple."""
    return [{
        "id": "T1",
        "name": "Tâche 1",
        "status": TaskStatus.IN_PROGRESS,
        "start_date": date.today() - timedelta(days=5),
        "end_date": date.today() + timedelta(days=5),
        "progress": 50,
        "metrics": {
            "quality": 0.85,
            "complexity": 3
        }
    }, {
        "id": "T2",
        "name": "Tâche 2",
        "status": TaskStatus.COMPLETED,
        "start_date": date.today() - timedelta(days=10),
        "end_date": date.today() - timedelta(days=2),
        "progress": 100,
        "metrics": {
            "quality": 0.95,
            "complexity": 2
        }
    }]

@pytest.fixture
def sample_resources():
    """Fixture pour les ressources exemple."""
    return [{
        "id": "R1",
        "type": ResourceType.HUMAN,
        "efficiency": 0.9,
        "cost": 1000.0
    }, {
        "id": "R2",
        "type": ResourceType.MATERIAL,
        "efficiency": 0.95,
        "cost": 500.0
    }]

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

class TestPerformanceAnalyzer:
    """Tests pour PerformanceAnalyzer."""

    async def test_analyze_performance_with_cache(
        self,
        analyzer,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de l'analyse avec cache."""
        # Configuration
        project_id = "P1"
        cached_result = {
            "kpis": {
                "schedule_performance": 0.85,
                "cost_performance": 0.9,
                "resource_efficiency": 0.88,
                "quality_score": 0.92,
                "risk_score": 0.15
            },
            "trends": {},
            "predictions": {},
            "recommendations": []
        }
        analyzer.cache.get.return_value = cached_result
        
        # Exécution
        result = await analyzer.analyze_performance(project_id)
        
        # Vérifications
        assert result == cached_result
        analyzer.cache.get.assert_called_once()

    async def test_analyze_performance_without_cache(
        self,
        analyzer,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de l'analyse sans cache."""
        # Configuration
        project_id = "P1"
        analyzer.cache.get.return_value = None
        analyzer._get_tasks = AsyncMock(return_value=sample_tasks)
        analyzer._get_resources = AsyncMock(return_value=sample_resources)
        analyzer._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        result = await analyzer.analyze_performance(project_id)
        
        # Vérifications
        assert "kpis" in result
        assert all(
            kpi in result["kpis"]
            for kpi in [
                "schedule_performance",
                "cost_performance",
                "resource_efficiency",
                "quality_score",
                "risk_score"
            ]
        )
        
        assert "trends" in result
        assert all(
            trend in result["trends"]
            for trend in [
                "velocity",
                "completion_rate",
                "resource_usage",
                "quality_trend",
                "risk_trend"
            ]
        )
        
        assert "predictions" in result
        assert all(
            pred in result["predictions"]
            for pred in [
                "completion_date",
                "final_cost",
                "quality_forecast",
                "risk_forecast"
            ]
        )
        
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

    def test_calculate_schedule_performance(
        self,
        analyzer,
        sample_tasks
    ):
        """Test du calcul de performance planning."""
        # Exécution
        performance = analyzer._calculate_schedule_performance(sample_tasks)
        
        # Vérifications
        assert isinstance(performance, float)
        assert 0 <= performance <= 1
        
        # Test avec tâches vides
        assert analyzer._calculate_schedule_performance([]) == 0.0

    def test_calculate_cost_performance(
        self,
        analyzer,
        sample_tasks,
        sample_resources
    ):
        """Test du calcul de performance coût."""
        # Exécution
        performance = analyzer._calculate_cost_performance(
            sample_tasks,
            sample_resources
        )
        
        # Vérifications
        assert isinstance(performance, float)
        assert 0 <= performance <= 1
        
        # Test avec données vides
        assert analyzer._calculate_cost_performance([], []) == 0.0

    def test_calculate_resource_efficiency(
        self,
        analyzer,
        sample_tasks,
        sample_resources
    ):
        """Test du calcul d'efficacité des ressources."""
        # Exécution
        efficiency = analyzer._calculate_resource_efficiency(
            sample_tasks,
            sample_resources
        )
        
        # Vérifications
        assert isinstance(efficiency, float)
        assert 0 <= efficiency <= 1
        
        # Test avec données vides
        assert analyzer._calculate_resource_efficiency([], []) == 0.0

    def test_calculate_quality_score(
        self,
        analyzer,
        sample_tasks,
        sample_iot_data
    ):
        """Test du calcul du score qualité."""
        # Exécution
        quality = analyzer._calculate_quality_score(
            sample_tasks,
            sample_iot_data
        )
        
        # Vérifications
        assert isinstance(quality, float)
        assert 0 <= quality <= 1
        
        # Test avec données vides
        assert analyzer._calculate_quality_score([], {}) == 0.0

    def test_calculate_risk_score(
        self,
        analyzer,
        sample_tasks,
        sample_iot_data
    ):
        """Test du calcul du score de risque."""
        # Exécution
        risk = analyzer._calculate_risk_score(
            sample_tasks,
            sample_iot_data
        )
        
        # Vérifications
        assert isinstance(risk, float)
        assert 0 <= risk <= 1
        
        # Test avec tâches bloquées
        blocked_tasks = [
            {**task, "status": TaskStatus.BLOCKED}
            for task in sample_tasks
        ]
        blocked_risk = analyzer._calculate_risk_score(
            blocked_tasks,
            sample_iot_data
        )
        assert blocked_risk > risk

    def test_analyze_trends(
        self,
        analyzer,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de l'analyse des tendances."""
        # Test vélocité
        velocity = analyzer._analyze_velocity_trend(sample_tasks)
        assert all(k in velocity for k in ["current", "trend", "forecast"])
        
        # Test complétion
        completion = analyzer._analyze_completion_trend(sample_tasks)
        assert all(k in completion for k in ["current", "trend", "forecast"])
        
        # Test ressources
        resources = analyzer._analyze_resource_trend(sample_tasks, sample_resources)
        assert all(k in resources for k in ["current", "trend", "forecast"])
        
        # Test qualité
        quality = analyzer._analyze_quality_trend(sample_tasks, sample_iot_data)
        assert all(k in quality for k in ["current", "trend", "forecast"])
        
        # Test risque
        risk = analyzer._analyze_risk_trend(sample_tasks, sample_iot_data)
        assert all(k in risk for k in ["current", "trend", "forecast"])

    def test_predictions(
        self,
        analyzer,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test des prédictions."""
        trends = {
            "velocity": {"forecast": 0.5},
            "completion_rate": {"current": 0.5},
            "resource_usage": {"forecast": 0.8},
            "quality_trend": {"forecast": 0.9},
            "risk_trend": {"forecast": 0.2}
        }
        
        # Test date fin
        completion_date = analyzer._predict_completion_date(sample_tasks, trends)
        assert isinstance(completion_date, date)
        
        # Test coût final
        final_cost = analyzer._predict_final_cost(
            sample_tasks,
            sample_resources,
            trends
        )
        assert isinstance(final_cost, float)
        assert final_cost >= 0
        
        # Test qualité finale
        quality = analyzer._predict_quality(sample_tasks, sample_iot_data, trends)
        assert isinstance(quality, float)
        assert 0 <= quality <= 1
        
        # Test risque final
        risk = analyzer._predict_risk(sample_tasks, sample_iot_data, trends)
        assert isinstance(risk, float)
        assert 0 <= risk <= 1
