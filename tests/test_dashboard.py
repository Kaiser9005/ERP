"""
Tests d'intégration pour les endpoints du tableau de bord.
"""

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
    assert "alerts" in data  # Nouvelles alertes ML
    assert "predictions" in data  # Nouvelles prédictions ML

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

    # Vérification des alertes ML
    alerts = data["alerts"]
    assert isinstance(alerts, list)
    for alert in alerts:
        assert "type" in alert
        assert "message" in alert
        assert "priority" in alert
        assert alert["priority"] in [1, 2, 3]  # Priorités valides

    # Vérification des prédictions ML
    predictions = data["predictions"]
    assert isinstance(predictions, dict)
    assert "hr" in predictions
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions

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

def test_get_ml_predictions(
    client: TestClient,
    db: Session,
    test_user: dict,
    test_data: dict
):
    """Test de récupération des prédictions ML"""
    response = client.get("/api/v1/dashboard/predictions")
    assert response.status_code == 200
    
    predictions = response.json()
    
    # Vérification de la structure
    assert "hr" in predictions
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions

    # Vérification des prédictions RH
    hr = predictions["hr"]
    assert "absences_prediction" in hr
    assert "turnover_prediction" in hr
    assert "training_needs" in hr

    # Vérification des prédictions de production
    production = predictions["production"]
    assert "yield_prediction" in production
    assert "quality_prediction" in production
    assert "maintenance_prediction" in production

    # Vérification des prédictions financières
    finance = predictions["finance"]
    assert "revenue_prediction" in finance
    assert "expense_prediction" in finance
    assert "cash_flow_prediction" in finance

def test_get_critical_alerts(
    client: TestClient,
    db: Session,
    test_user: dict,
    test_data: dict
):
    """Test de récupération des alertes critiques"""
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    
    alerts = response.json()
    assert isinstance(alerts, list)
    
    if len(alerts) > 0:
        alert = alerts[0]
        assert "type" in alert
        assert "message" in alert
        assert "priority" in alert
        assert alert["priority"] in [1, 2, 3]

def test_get_module_details(
    client: TestClient,
    db: Session,
    test_user: dict,
    test_data: dict
):
    """Test de récupération des détails d'un module spécifique"""
    modules = ["hr", "production", "finance", "inventory"]
    
    for module in modules:
        response = client.get(f"/api/v1/dashboard/modules/{module}")
        assert response.status_code == 200
        
        data = response.json()
        assert "stats" in data
        assert "alerts" in data
        assert "predictions" in data
        
        # Vérification des données ML
        assert isinstance(data["alerts"], list)
        assert isinstance(data["predictions"], dict)

    # Test avec un module invalide
    response = client.get("/api/v1/dashboard/modules/invalid")
    assert response.status_code == 404
