import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def test_get_dashboard_stats(
    client: TestClient,
    db: Session,
    test_user: dict,
    test_data: dict
):
    """Test de récupération des statistiques du tableau de bord"""
    response = client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "production" in data
    assert "inventory" in data
    assert "finance" in data
    assert "hr" in data

    # Vérification des statistiques de production
    assert data["production"]["total"] > 0
    assert "variation" in data["production"]
    assert isinstance(data["production"]["variation"]["value"], (int, float))
    assert data["production"]["variation"]["type"] in ["increase", "decrease"]

    # Vérification des statistiques d'inventaire
    assert data["inventory"]["value"] > 0
    assert "variation" in data["inventory"]

    # Vérification des statistiques RH
    assert data["hr"]["activeEmployees"] >= 1  # Au moins l'utilisateur de test
    assert "variation" in data["hr"]

def test_get_recent_activities(
    client: TestClient,
    db: Session,
    test_user: dict,
    test_data: dict
):
    """Test de récupération des activités récentes"""
    response = client.get("/api/v1/activities/recent")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, list)
    assert len(activities) > 0

    # Vérification de la structure d'une activité
    activity = activities[0]
    assert "id" in activity
    assert "type" in activity
    assert "title" in activity
    assert "description" in activity
    assert "date" in activity
    assert "color" in activity

def test_get_weather_data(client: TestClient):
    """Test de récupération des données météorologiques"""
    response = client.get("/api/v1/weather/current")
    assert response.status_code == 200
    
    data = response.json()
    assert "temperature" in data
    assert "humidity" in data
    assert "windSpeed" in data
    assert "uvIndex" in data
    assert "forecast" in data

    # Vérification des valeurs
    assert isinstance(data["temperature"], (int, float))
    assert 0 <= data["humidity"] <= 100
    assert data["windSpeed"] >= 0
    assert data["uvIndex"] >= 0
    assert isinstance(data["forecast"], list)