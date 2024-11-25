"""Tests pour le service de monitoring IoT."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.iot_monitoring_service import IoTMonitoringService
from services.iot_service import IoTService
from services.weather_service import WeatherService
from services.production_ml_service import ProductionMLService

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def iot_service():
    """Fixture pour le service IoT."""
    return Mock(spec=IoTService)

@pytest.fixture
def weather_service():
    """Fixture pour le service météo."""
    return Mock(spec=WeatherService)

@pytest.fixture
def ml_service():
    """Fixture pour le service ML."""
    return Mock(spec=ProductionMLService)

@pytest.fixture
def monitoring_service(db_session, iot_service, weather_service, ml_service):
    """Fixture pour le service de monitoring."""
    return IoTMonitoringService(
        db=db_session,
        iot_service=iot_service,
        weather_service=weather_service,
        ml_service=ml_service
    )

@pytest.fixture
def sample_sensor():
    """Fixture pour un capteur exemple."""
    return IoTSensor(
        id=uuid4(),
        code="TEMP001",
        type=SensorType.TEMPERATURE_SOL,
        status=SensorStatus.ACTIF,
        parcelle_id=uuid4(),
        latitude=48.8566,
        longitude=2.3522,
        config={},
        seuils_alerte={
            "min": 10,
            "max": 30,
            "critique_min": 5,
            "critique_max": 35
        },
        intervalle_lecture=300
    )

class TestIoTMonitoringService:
    """Tests pour IoTMonitoringService."""

    async def test_get_parcelle_monitoring(self, monitoring_service, sample_sensor):
        """Test de récupération des données de monitoring d'une parcelle."""
        # Configuration des mocks
        monitoring_service.iot_service.get_sensors_by_parcelle.return_value = [sample_sensor]
        monitoring_service.iot_service.check_sensor_health.return_value = {
            "status": SensorStatus.ACTIF,
            "message": "Capteur fonctionnel",
            "battery_level": 85,
            "signal_quality": 90,
            "last_reading": datetime.utcnow()
        }
        
        # Exécution
        result = await monitoring_service.get_parcelle_monitoring(
            parcelle_id=uuid4(),
            start_date=datetime.utcnow() - timedelta(days=1),
            end_date=datetime.utcnow()
        )
        
        # Vérifications
        assert result["parcelle_id"] is not None
        assert "capteurs" in result
        assert len(result["capteurs"]) == 1
        assert result["capteurs"][0]["status"] == SensorStatus.ACTIF

    async def test_get_monitoring_dashboard(self, monitoring_service, sample_sensor):
        """Test de récupération du dashboard de monitoring."""
        # Configuration des mocks
        monitoring_service.iot_service.get_sensors_by_parcelle.return_value = [sample_sensor]
        monitoring_service.weather_service.get_forecast.return_value = {
            "daily": [{"temp": 20, "humidity": 65}]
        }
        monitoring_service.ml_service.predict_conditions.return_value = {
            "predictions": [{"temp": 22, "probability": 0.8}]
        }
        
        # Exécution
        result = await monitoring_service.get_monitoring_dashboard(uuid4())
        
        # Vérifications
        assert "temps_reel" in result
        assert "historique" in result
        assert "predictions" in result
        assert "maintenance" in result

    async def test_get_maintenance_recommendations(self, monitoring_service, sample_sensor):
        """Test de récupération des recommandations de maintenance."""
        # Configuration des mocks
        monitoring_service.iot_service.get_sensors_by_parcelle.return_value = [sample_sensor]
        monitoring_service.iot_service.check_sensor_health.return_value = {
            "status": SensorStatus.MAINTENANCE,
            "message": "Batterie faible",
            "battery_level": 15,
            "signal_quality": 90,
            "last_reading": datetime.utcnow()
        }
        
        # Exécution
        result = await monitoring_service._get_maintenance_recommendations(uuid4())
        
        # Vérifications
        assert len(result) > 0
        assert result[0]["priorite"] == "moyenne"
        assert "batterie" in result[0]["raison"].lower()

    async def test_system_health(self, monitoring_service, sample_sensor):
        """Test de vérification de la santé du système."""
        # Configuration des mocks
        monitoring_service.iot_service.get_sensors_by_parcelle.return_value = [sample_sensor]
        monitoring_service.iot_service.check_sensor_health.return_value = {
            "status": SensorStatus.ACTIF,
            "message": "Capteur fonctionnel",
            "battery_level": 85,
            "signal_quality": 90,
            "last_reading": datetime.utcnow()
        }
        
        # Exécution
        result = await monitoring_service._get_system_health([sample_sensor])
        
        # Vérifications
        assert result["total_capteurs"] == 1
        assert result["capteurs_actifs"] == 1
        assert result["sante_globale"] == 1.0

    async def test_error_handling(self, monitoring_service):
        """Test de la gestion des erreurs."""
        # Configuration du mock pour lever une exception
        monitoring_service.iot_service.get_sensors_by_parcelle.side_effect = Exception("Erreur test")
        
        # Vérification que l'exception est bien propagée
        with pytest.raises(Exception) as exc_info:
            await monitoring_service.get_parcelle_monitoring(uuid4())
        
        assert str(exc_info.value) == "Erreur test"

    async def test_ml_predictions(self, monitoring_service, sample_sensor):
        """Test des prédictions ML."""
        # Configuration des mocks
        monitoring_service.iot_service.get_sensors_by_parcelle.return_value = [sample_sensor]
        monitoring_service.iot_service.get_sensor_readings.return_value = [
            {"timestamp": datetime.utcnow(), "valeur": 25}
        ]
        monitoring_service.weather_service.get_forecast.return_value = {
            "daily": [{"temp": 20, "humidity": 65}]
        }
        monitoring_service.ml_service.predict_conditions.return_value = {
            "predictions": [{"temp": 22, "probability": 0.8}],
            "factors": ["temperature", "humidité"],
            "recommendations": ["Surveillance recommandée"]
        }
        
        # Exécution
        result = await monitoring_service._get_ml_predictions(
            parcelle_id=uuid4(),
            sensors=[sample_sensor],
            reference_date=datetime.utcnow()
        )
        
        # Vérifications
        assert "predictions" in result
        assert len(result["predictions"]) > 0
        assert "probability" in result["predictions"][0]
        assert result["predictions"][0]["probability"] == 0.8
