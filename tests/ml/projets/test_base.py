"""Tests pour les fonctionnalités ML de base."""

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
from services.ml.projets.base import ProjectsMLService

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
def ml_service(db_session, weather_service, iot_service, cache_service):
    """Fixture pour le service ML."""
    service = ProjectsMLService(db_session)
    service.weather_service = weather_service
    service.iot_service = iot_service
    service.cache = cache_service
    return service

@pytest.fixture
def sample_tasks():
    """Fixture pour les tâches exemple."""
    return [
        {
            "id": "T1",
            "name": "Tâche 1",
            "status": TaskStatus.IN_PROGRESS,
            "progress": 0.5,
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=7),
            "dependencies": [],
            "resources": ["R1"],
            "metrics": {"complexity": 3}
        },
        {
            "id": "T2",
            "name": "Tâche 2",
            "status": TaskStatus.COMPLETED,
            "progress": 1.0,
            "start_date": date.today() - timedelta(days=7),
            "end_date": date.today(),
            "dependencies": ["T1"],
            "resources": ["R2"],
            "metrics": {"complexity": 2}
        }
    ]

@pytest.fixture
def sample_resources():
    """Fixture pour les ressources exemple."""
    return [
        {
            "id": "R1",
            "type": ResourceType.HUMAN,
            "name": "Resource 1",
            "availability": 0.8,
            "efficiency": 0.9,
            "cost": 1000
        },
        {
            "id": "R2",
            "type": ResourceType.MATERIAL,
            "name": "Resource 2",
            "availability": 1.0,
            "efficiency": 0.95,
            "cost": 500
        }
    ]

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
                "battery_level": 85,
                "signal_quality": 90
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
                "battery_level": 90,
                "signal_quality": 95
            }
        }
    }

class TestProjectsMLService:
    """Tests pour ProjectsMLService."""

    async def test_predict_project_success_with_cache(
        self,
        ml_service,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de la prédiction avec cache."""
        # Configuration du cache
        cached_prediction = {
            "probability": 0.8,
            "risk_factors": [],
            "recommendations": []
        }
        ml_service.cache.get.return_value = cached_prediction
        
        # Exécution
        result = await ml_service.predict_project_success("P1")
        
        # Vérifications
        assert result == cached_prediction
        ml_service.cache.get.assert_called_once()

    async def test_predict_project_success_without_cache(
        self,
        ml_service,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test de la prédiction sans cache."""
        # Configuration des mocks
        ml_service.cache.get.return_value = None
        ml_service._get_project_tasks = AsyncMock(return_value=sample_tasks)
        ml_service._get_project_resources = AsyncMock(return_value=sample_resources)
        ml_service._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        result = await ml_service.predict_project_success("P1")
        
        # Vérifications
        assert "probability" in result
        assert isinstance(result["probability"], float)
        assert 0 <= result["probability"] <= 1
        
        assert "risk_factors" in result
        assert isinstance(result["risk_factors"], list)
        assert all(
            {"factor", "impact", "description"}.issubset(rf.keys())
            for rf in result["risk_factors"]
        )
        
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
        assert all(
            {"type", "priority", "description", "actions"}.issubset(r.keys())
            for r in result["recommendations"]
        )

    def test_calculate_success_features(
        self,
        ml_service,
        sample_tasks,
        sample_resources,
        sample_iot_data
    ):
        """Test du calcul des features."""
        # Configuration
        weather_data = {
            "impact_score": 0.7,
            "risk_factors": ["RAIN", "WIND"],
            "affected_tasks": ["T1"],
            "precipitation_risk": 0.6,
            "temperature_risk": 0.3
        }
        
        # Exécution
        features = ml_service._calculate_success_features(
            sample_tasks,
            sample_resources,
            weather_data,
            sample_iot_data
        )
        
        # Vérifications
        assert isinstance(features, np.ndarray)
        assert features.ndim == 2  # Features normalisées (2D array)
        assert features.shape[1] > 0  # Au moins une feature

    def test_get_feature_name(self, ml_service):
        """Test de la récupération des noms de features."""
        # Test features de base
        assert "Nombre_Taches" == ml_service._get_feature_name(0)
        assert "Progression_Moyenne" == ml_service._get_feature_name(1)
        
        # Test features IoT
        sensor_feature_index = 15  # Après les features de base
        feature_name = ml_service._get_feature_name(sensor_feature_index)
        assert any(t.value in feature_name for t in SensorType)
        assert any(
            metric in feature_name
            for metric in ["Moyenne", "Minimum", "Maximum", "Statut", "Batterie"]
        )

    def test_get_risk_description(self, ml_service):
        """Test de la génération des descriptions de risque."""
        # Test différents types de features
        assert "insuffisante" in ml_service._get_risk_description(
            0, 0.3
        ).lower()  # Tâches basse
        assert "optimale" in ml_service._get_risk_description(
            5, 0.8
        ).lower()  # Ressources haute
        assert "élevés" in ml_service._get_risk_description(
            10, 0.8
        ).lower()  # Météo haute
        
        # Test feature IoT
        iot_feature_index = 15
        assert "capteurs" in ml_service._get_risk_description(
            iot_feature_index,
            0.3
        ).lower()
