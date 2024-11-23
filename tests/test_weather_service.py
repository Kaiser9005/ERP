import pytest
from datetime import datetime, timezone
from services.weather_service import WeatherService
import httpx
from unittest.mock import patch, MagicMock, AsyncMock
import json
import redis


@pytest.fixture
def weather_service():
    """Fixture pour le service météo avec Redis mocké"""
    with patch('redis.Redis') as mock_redis:
        service = WeatherService()
        # Configuration du mock Redis
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        service.redis_client = mock_redis_instance
        # Mock du service de notification
        service.notification_service = AsyncMock()
        return service


@pytest.mark.asyncio
async def test_get_current_weather_from_cache(weather_service):
    """Test de récupération des données depuis le cache"""
    cached_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": 25.5,
        "humidity": 80,
        "precipitation": 0.5,
        "wind_speed": 15,
        "conditions": "Partiellement nuageux",
        "uv_index": 6,
        "cloud_cover": 45
    }

    # Configuration du mock Redis pour retourner des données en cache
    weather_service.redis_client.get.return_value = json.dumps(cached_data)

    result = await weather_service.get_current_weather()
    assert result == cached_data
    weather_service.redis_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_current_weather_api_with_cache(weather_service):
    """Test de récupération et mise en cache des données API"""
    # Configuration du mock Redis pour simuler un cache vide
    weather_service.redis_client.get.return_value = None

    mock_response = {
        "currentConditions": {
            "temp": 25.5,
            "humidity": 80,
            "precip": 0.5,
            "windspeed": 15,
            "conditions": "Partiellement nuageux",
            "uvindex": 6,
            "cloudcover": 45
        }
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )

        weather_data = await weather_service.get_current_weather()

        assert weather_data["temperature"] == 25.5
        weather_service.redis_client.setex.assert_called_once()


@pytest.mark.asyncio
async def test_retry_mechanism(weather_service):
    """Test du mécanisme de retry"""
    with patch("httpx.AsyncClient.get") as mock_get:
        # Simuler 2 échecs suivis d'un succès
        mock_get.side_effect = [
            httpx.HTTPError("Erreur 1"),
            httpx.HTTPError("Erreur 2"),
            MagicMock(
                status_code=200,
                json=lambda: {"currentConditions": {"temp": 25.5}}
            )
        ]

        weather_data = await weather_service.get_current_weather()

        assert weather_data["temperature"] == 25.5
        assert mock_get.call_count == 3


@pytest.mark.asyncio
async def test_timeout_handling(weather_service):
    """Test de la gestion des timeouts"""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Timeout")

        weather_data = await weather_service.get_current_weather()

        # Vérifie qu'on obtient les données de fallback
        assert weather_data["temperature"] == 25.0
        # Vérifie que la notification d'erreur a été envoyée
        weather_service.notification_service.send_notification.assert_called_once()


@pytest.mark.asyncio
async def test_high_risk_notification(weather_service):
    """Test de l'envoi de notification pour risque élevé"""
    current_mock = {
        "currentConditions": {
            "temp": 37,
            "humidity": 85,
            "precip": 25,
            "windspeed": 20,
            "conditions": "Pluie forte",
            "uvindex": 7,
            "cloudcover": 90
        }
    }

    forecast_mock = {
        "resolvedAddress": "Ebondi,Cameroon",
        "days": [
            {
                "datetime": "2024-01-20",
                "tempmax": 38,
                "tempmin": 23,
                "precip": 22,
                "humidity": 80,
                "conditions": "Pluie forte"
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = [
            MagicMock(status_code=200, json=lambda: current_mock),
            MagicMock(status_code=200, json=lambda: forecast_mock)
        ]

        metrics = await weather_service.get_agricultural_metrics()

        # Vérifie que la notification a été envoyée pour le risque élevé
        weather_service.notification_service.send_notification.assert_called_once()
        call_args = weather_service.notification_service.send_notification.call_args[0]
        assert call_args[0] == "production"
        assert "ALERTE MÉTÉO" in call_args[2]


@pytest.mark.asyncio
async def test_get_forecast_with_cache(weather_service):
    """Test des prévisions avec cache"""
    forecast_data = {
        "location": "Ebondi,Cameroon",
        "days": [
            {
                "date": "2024-01-20",
                "temp_max": 32,
                "temp_min": 22,
                "precipitation": 0.8,
                "humidity": 75,
                "conditions": "Pluie légère",
                "description": "Journée nuageuse avec pluie légère"
            }
        ]
    }

    # Test avec données en cache
    weather_service.redis_client.get.return_value = json.dumps(forecast_data)
    result = await weather_service.get_forecast(1)
    assert result == forecast_data

    # Test sans cache (appel API)
    weather_service.redis_client.get.return_value = None
    mock_response = {
        "resolvedAddress": "Ebondi,Cameroon",
        "days": [
            {
                "datetime": "2024-01-20",
                "tempmax": 32,
                "tempmin": 22,
                "precip": 0.8,
                "humidity": 75,
                "conditions": "Pluie légère",
                "description": "Journée nuageuse avec pluie légère"
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )

        result = await weather_service.get_forecast(1)
        assert result["location"] == "Ebondi,Cameroon"
        weather_service.redis_client.setex.assert_called_once()


@pytest.mark.asyncio
async def test_error_handling_and_notification(weather_service):
    """Test de la gestion des erreurs et notifications"""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.RequestError("Erreur réseau")

        await weather_service.get_current_weather()

        # Vérifie l'envoi de notification d'erreur
        notification_call = weather_service.notification_service.send_notification.call_args[0]
        assert notification_call[0] == "admin"
        assert "Erreur Service Météo" in notification_call[1]
        assert "Erreur réseau" in notification_call[2]


def test_analyze_precipitation():
    """Test de l'analyse des risques liés aux précipitations"""
    weather_service = WeatherService()

    # Test risque élevé
    high_risk = weather_service._analyze_precipitation(25, [20, 22, 18])
    assert high_risk["level"] == "HIGH"
    assert "inondation" in high_risk["message"].lower()

    # Test risque moyen
    medium_risk = weather_service._analyze_precipitation(15, [12, 8, 10])
    assert medium_risk["level"] == "MEDIUM"
    assert "surveillance" in medium_risk["message"].lower()

    # Test risque faible
    low_risk = weather_service._analyze_precipitation(5, [3, 4, 6])
    assert low_risk["level"] == "LOW"
    assert "normales" in low_risk["message"].lower()


def test_analyze_temperature():
    """Test de l'analyse des risques liés à la température"""
    weather_service = WeatherService()

    # Test risque élevé
    high_risk = weather_service._analyze_temperature(37, [36, 38, 35])
    assert high_risk["level"] == "HIGH"
    assert "stress thermique" in high_risk["message"].lower()

    # Test risque moyen
    medium_risk = weather_service._analyze_temperature(32, [31, 33, 32])
    assert medium_risk["level"] == "MEDIUM"
    assert "surveillance" in medium_risk["message"].lower()

    # Test risque faible
    low_risk = weather_service._analyze_temperature(28, [27, 29, 28])
    assert low_risk["level"] == "LOW"
    assert "normale" in low_risk["message"].lower()


def test_generate_recommendations():
    """Test de la génération des recommandations"""
    weather_service = WeatherService()

    # Test recommandations pour risques élevés
    high_risks = weather_service._generate_recommendations(
        {"level": "HIGH", "message": "Risque d'inondation"},
        {"level": "HIGH", "message": "Risque de stress thermique"}
    )
    assert len(high_risks) >= 4
    assert any("drainage" in rec.lower() for rec in high_risks)
    assert any("irrigation" in rec.lower() for rec in high_risks)

    # Test recommandations pour risques moyens
    medium_risks = weather_service._generate_recommendations(
        {"level": "MEDIUM", "message": "Précipitations modérées"},
        {"level": "MEDIUM", "message": "Températures élevées"}
    )
    assert len(medium_risks) >= 2
    assert any("surveillance" in rec.lower() for rec in medium_risks)

    # Test recommandations pour risques faibles
    low_risks = weather_service._generate_recommendations(
        {"level": "LOW", "message": "Conditions normales"},
        {"level": "LOW", "message": "Températures normales"}
    )
    assert len(low_risks) == 1
    assert "favorables" in low_risks[0].lower()
