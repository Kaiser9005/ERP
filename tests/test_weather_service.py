import pytest
from services.weather_service import WeatherService
import aiohttp
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_get_current_weather():
    """Test du service météo avec mock des appels API"""
    weather_service = WeatherService()

    # Mock de la réponse de l'API météo
    mock_weather_response = {
        "main": {
            "temp": 25.5,
            "humidity": 80
        },
        "wind": {
            "speed": 5.0
        }
    }

    mock_uv_response = {
        "value": 8
    }

    mock_forecast_response = {
        "list": [
            {
                "dt_txt": "2024-01-20 12:00:00",
                "main": {"temp": 26.5},
                "pop": 0.3
            }
        ]
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        # Configuration des mocks
        mock_weather = MagicMock()
        mock_weather.status = 200
        mock_weather.__aenter__.return_value = mock_weather
        mock_weather.json.return_value = mock_weather_response

        mock_uv = MagicMock()
        mock_uv.status = 200
        mock_uv.__aenter__.return_value = mock_uv
        mock_uv.json.return_value = mock_uv_response

        mock_forecast = MagicMock()
        mock_forecast.status = 200
        mock_forecast.__aenter__.return_value = mock_forecast
        mock_forecast.json.return_value = mock_forecast_response

        mock_get.side_effect = [mock_weather, mock_uv, mock_forecast]

        # Test du service
        weather_data = await weather_service.get_current_weather()

        assert weather_data["temperature"] == 25.5
        assert weather_data["humidity"] == 80
        assert weather_data["windSpeed"] == 18.0  # 5.0 * 3.6
        assert weather_data["uvIndex"] == 8
        assert len(weather_data["forecast"]) > 0

@pytest.mark.asyncio
async def test_weather_service_fallback():
    """Test du comportement en cas d'erreur API"""
    weather_service = WeatherService()

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status = 500
        mock_response.__aenter__.return_value = mock_response
        mock_get.return_value = mock_response

        # Test du service avec erreur
        weather_data = await weather_service.get_current_weather()

        # Vérification des données de fallback
        assert weather_data["temperature"] == 25.0
        assert weather_data["humidity"] == 80
        assert weather_data["windSpeed"] == 5.0
        assert weather_data["uvIndex"] == 5
        assert len(weather_data["forecast"]) == 0