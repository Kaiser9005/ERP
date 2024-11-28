"""Tests pour l'analyse météo."""

import pytest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.ml.projets.weather import WeatherAnalyzer

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
def analyzer(db_session, weather_service, iot_service, cache_service):
    """Fixture pour l'analyseur."""
    service = WeatherAnalyzer(db_session)
    service.weather_service = weather_service
    service.iot_service = iot_service
    service.cache = cache_service
    return service

@pytest.fixture
def sample_tasks():
    """Fixture pour les tâches exemple."""
    return [{
        "id": "T1",
        "name": "Tâche 1",
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=5),
        "weather_conditions": ["TEMPERATURE", "RAIN"],
        "flexibility": 0.7
    }, {
        "id": "T2",
        "name": "Tâche 2",
        "start_date": date.today() + timedelta(days=3),
        "end_date": date.today() + timedelta(days=8),
        "weather_conditions": ["WIND", "FROST"],
        "flexibility": 0.3
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

class TestWeatherAnalyzer:
    """Tests pour WeatherAnalyzer."""

    async def test_analyze_weather_impact_with_cache(
        self,
        analyzer,
        sample_tasks,
        sample_weather,
        sample_iot_data
    ):
        """Test de l'analyse avec cache."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        cached_result = {
            "impact_score": 0.7,
            "affected_tasks": [{
                "task_id": "T1",
                "impact": "HIGH",
                "conditions": ["RAIN"]
            }],
            "risk_periods": [{
                "period": start_date.strftime("%Y-%m"),
                "risk": "HIGH",
                "conditions": ["RAIN"]
            }],
            "alternatives": [{
                "task_id": "T1",
                "original_date": start_date,
                "alternative_date": start_date + timedelta(days=2),
                "reason": "Éviter RAIN"
            }]
        }
        analyzer.cache.get.return_value = cached_result
        
        # Exécution
        result = await analyzer.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert result == cached_result
        analyzer.cache.get.assert_called_once()

    async def test_analyze_weather_impact_without_cache(
        self,
        analyzer,
        sample_tasks,
        sample_weather,
        sample_iot_data
    ):
        """Test de l'analyse sans cache."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        analyzer.cache.get.return_value = None
        analyzer._get_weather_sensitive_tasks = AsyncMock(return_value=sample_tasks)
        analyzer.weather_service.get_forecast.return_value = sample_weather
        analyzer._get_iot_data = AsyncMock(return_value=sample_iot_data)
        
        # Exécution
        result = await analyzer.analyze_weather_impact(
            project_id,
            start_date,
            end_date
        )
        
        # Vérifications
        assert "impact_score" in result
        assert isinstance(result["impact_score"], float)
        assert 0 <= result["impact_score"] <= 1
        
        assert "affected_tasks" in result
        assert isinstance(result["affected_tasks"], list)
        assert all(
            {"task_id", "impact", "conditions"}.issubset(t.keys())
            for t in result["affected_tasks"]
        )
        
        assert "risk_periods" in result
        assert isinstance(result["risk_periods"], list)
        assert all(
            {"period", "risk", "conditions"}.issubset(p.keys())
            for p in result["risk_periods"]
        )
        
        assert "alternatives" in result
        assert isinstance(result["alternatives"], list)
        assert all(
            {
                "task_id",
                "original_date",
                "alternative_date",
                "reason"
            }.issubset(a.keys())
            for a in result["alternatives"]
        )

    def test_evaluate_weather_risk(
        self,
        analyzer,
        sample_iot_data
    ):
        """Test de l'évaluation des risques météo."""
        # Configuration
        conditions = {
            "temperature": 35.0,
            "temperature_min": 1.0,
            "precipitation": 25.0,
            "wind_speed": 40.0
        }
        
        # Test température
        risk = analyzer._evaluate_weather_risk(
            conditions,
            ["TEMPERATURE"],
            sample_iot_data
        )
        assert risk > 0.7  # Température élevée
        
        # Test pluie
        risk = analyzer._evaluate_weather_risk(
            conditions,
            ["RAIN"],
            sample_iot_data
        )
        assert risk > 0.7  # Fortes précipitations
        
        # Test vent
        risk = analyzer._evaluate_weather_risk(
            conditions,
            ["WIND"],
            sample_iot_data
        )
        assert risk > 0.7  # Vent fort
        
        # Test gel
        conditions["temperature_min"] = -2.0
        risk = analyzer._evaluate_weather_risk(
            conditions,
            ["FROST"],
            sample_iot_data
        )
        assert risk > 0.7  # Risque de gel

    def test_evaluate_temperature_risk(
        self,
        analyzer,
        sample_iot_data
    ):
        """Test de l'évaluation des risques de température."""
        # Test température élevée
        risk = analyzer._evaluate_temperature_risk(
            {"temperature": 35.0},
            sample_iot_data
        )
        assert risk > 0.7
        
        # Test température normale
        risk = analyzer._evaluate_temperature_risk(
            {"temperature": 22.0},
            sample_iot_data
        )
        assert risk < 0.5
        
        # Test température basse
        risk = analyzer._evaluate_temperature_risk(
            {"temperature": 5.0},
            sample_iot_data
        )
        assert risk > 0.7

    def test_evaluate_rain_risk(
        self,
        analyzer,
        sample_iot_data
    ):
        """Test de l'évaluation des risques de pluie."""
        # Test fortes pluies
        risk = analyzer._evaluate_rain_risk(
            {"precipitation": 25.0},
            sample_iot_data
        )
        assert risk > 0.7
        
        # Test pluies modérées
        risk = analyzer._evaluate_rain_risk(
            {"precipitation": 12.0},
            sample_iot_data
        )
        assert 0.3 < risk < 0.7
        
        # Test pluies faibles
        risk = analyzer._evaluate_rain_risk(
            {"precipitation": 2.0},
            sample_iot_data
        )
        assert risk < 0.3

    def test_evaluate_wind_risk(
        self,
        analyzer,
        sample_iot_data
    ):
        """Test de l'évaluation des risques de vent."""
        # Test vent violent
        risk = analyzer._evaluate_wind_risk(
            {"wind_speed": 55.0},
            sample_iot_data
        )
        assert risk > 0.7
        
        # Test vent modéré
        risk = analyzer._evaluate_wind_risk(
            {"wind_speed": 25.0},
            sample_iot_data
        )
        assert 0.3 < risk < 0.7
        
        # Test vent faible
        risk = analyzer._evaluate_wind_risk(
            {"wind_speed": 15.0},
            sample_iot_data
        )
        assert risk < 0.3

    def test_evaluate_frost_risk(
        self,
        analyzer,
        sample_iot_data
    ):
        """Test de l'évaluation des risques de gel."""
        # Test gel
        risk = analyzer._evaluate_frost_risk(
            {"temperature_min": -2.0},
            sample_iot_data
        )
        assert risk > 0.7
        
        # Test proche gel
        risk = analyzer._evaluate_frost_risk(
            {"temperature_min": 3.0},
            sample_iot_data
        )
        assert 0.3 < risk < 0.7
        
        # Test sans gel
        risk = analyzer._evaluate_frost_risk(
            {"temperature_min": 10.0},
            sample_iot_data
        )
        assert risk < 0.3

    def test_get_risk_conditions(self, analyzer):
        """Test de l'identification des conditions à risque."""
        # Configuration
        condition = {
            "temperature": 35.0,
            "temperature_min": 1.0,
            "precipitation": 25.0,
            "wind_speed": 40.0
        }
        
        # Exécution
        risks = analyzer._get_risk_conditions(condition)
        
        # Vérifications
        assert "TEMPERATURE" in risks  # Température élevée
        assert "RAIN" in risks  # Fortes précipitations
        assert "WIND" in risks  # Vent fort
        
        # Test gel
        condition["temperature_min"] = -2.0
        risks = analyzer._get_risk_conditions(condition)
        assert "FROST" in risks
