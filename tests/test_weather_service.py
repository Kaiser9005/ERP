import pytest
from datetime import datetime, timezone
from services.weather_service import WeatherService
import httpx
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_get_current_weather():
    """Test de récupération des conditions météo actuelles"""
    weather_service = WeatherService()

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
        assert weather_data["humidity"] == 80
        assert weather_data["precipitation"] == 0.5
        assert weather_data["wind_speed"] == 15
        assert weather_data["conditions"] == "Partiellement nuageux"
        assert weather_data["uv_index"] == 6
        assert weather_data["cloud_cover"] == 45

@pytest.mark.asyncio
async def test_get_forecast():
    """Test de récupération des prévisions"""
    weather_service = WeatherService()

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
            },
            {
                "datetime": "2024-01-21",
                "tempmax": 30,
                "tempmin": 21,
                "precip": 0.2,
                "humidity": 70,
                "conditions": "Partiellement nuageux",
                "description": "Journée partiellement nuageuse"
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response
        )

        forecast_data = await weather_service.get_forecast(2)

        assert forecast_data["location"] == "Ebondi,Cameroon"
        assert len(forecast_data["days"]) == 2
        assert forecast_data["days"][0]["temp_max"] == 32
        assert forecast_data["days"][1]["conditions"] == "Partiellement nuageux"

@pytest.mark.asyncio
async def test_get_agricultural_metrics():
    """Test des métriques agricoles et analyses"""
    weather_service = WeatherService()

    current_mock = {
        "currentConditions": {
            "temp": 34,
            "humidity": 85,
            "precip": 15,
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
                "tempmax": 33,
                "tempmin": 23,
                "precip": 12,
                "humidity": 80,
                "conditions": "Pluie"
            },
            {
                "datetime": "2024-01-21",
                "tempmax": 32,
                "tempmin": 22,
                "precip": 8,
                "humidity": 75,
                "conditions": "Pluie légère"
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = [
            MagicMock(status_code=200, json=lambda: current_mock),
            MagicMock(status_code=200, json=lambda: forecast_mock)
        ]

        metrics = await weather_service.get_agricultural_metrics()

        # Vérification des conditions actuelles
        assert metrics["current_conditions"]["temperature"] == 34
        assert metrics["current_conditions"]["precipitation"] == 15

        # Vérification des analyses de risques
        assert metrics["risks"]["precipitation"]["level"] == "HIGH"
        assert metrics["risks"]["temperature"]["level"] == "MEDIUM"
        assert "Risque d'inondation" in metrics["risks"]["precipitation"]["message"]

        # Vérification des recommandations
        recommendations = metrics["recommendations"]
        assert any("drainage" in rec.lower() for rec in recommendations)
        assert any("irrigation" in rec.lower() for rec in recommendations)

@pytest.mark.asyncio
async def test_weather_service_fallback():
    """Test du comportement en cas d'erreur API"""
    weather_service = WeatherService()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.HTTPError("API Error")

        weather_data = await weather_service.get_current_weather()

        # Vérification des données de fallback
        assert weather_data["temperature"] == 25.0
        assert weather_data["humidity"] == 80
        assert weather_data["wind_speed"] == 5.0
        assert weather_data["conditions"] == "Partiellement nuageux"
        assert weather_data["uv_index"] == 5
        assert weather_data["cloud_cover"] == 50

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
