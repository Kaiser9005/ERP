"""
Tests end-to-end pour le tableau de bord ML.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

@pytest.mark.e2e
def test_tableau_bord_ml_e2e(client: TestClient, test_user: dict):
    """Test end-to-end du tableau de bord ML"""
    # Authentification
    response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Récupération des données du tableau de bord
    response = client.get("/api/v1/dashboard/unified", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Vérification de la structure des données
    assert "modules" in data
    assert "alerts" in data
    assert "predictions" in data
    assert "timestamp" in data

    # Vérification des alertes
    alerts = data["alerts"]
    assert isinstance(alerts, list)
    if len(alerts) > 0:
        alert = alerts[0]
        assert "type" in alert
        assert "message" in alert
        assert "priority" in alert
        assert alert["priority"] in [1, 2, 3]

    # Vérification des prédictions
    predictions = data["predictions"]
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions
    assert "hr" in predictions

    # Test des endpoints spécifiques ML
    
    # Prédictions par module
    modules = ["production", "finance", "inventory", "hr"]
    for module in modules:
        response = client.get(f"/api/v1/ml/predictions/{module}", headers=headers)
        assert response.status_code == 200
        module_predictions = response.json()
        assert isinstance(module_predictions, dict)

    # Alertes critiques
    response = client.get("/api/v1/ml/alerts/critical", headers=headers)
    assert response.status_code == 200
    critical_alerts = response.json()
    assert isinstance(critical_alerts, list)

    # Recommandations ML
    response = client.get("/api/v1/ml/recommendations", headers=headers)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)
    if len(recommendations) > 0:
        recommendation = recommendations[0]
        assert "module" in recommendation
        assert "action" in recommendation
        assert "confidence" in recommendation
        assert 0 <= recommendation["confidence"] <= 1

@pytest.mark.e2e
def test_tableau_bord_ml_error_handling(client: TestClient, test_user: dict):
    """Test de la gestion des erreurs du tableau de bord ML"""
    # Authentification
    response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test avec un module invalide
    response = client.get("/api/v1/ml/predictions/invalid_module", headers=headers)
    assert response.status_code == 404

    # Test avec des paramètres invalides
    response = client.get("/api/v1/ml/predictions/production?date_range=invalid", headers=headers)
    assert response.status_code == 400

    # Test avec un token invalide
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/dashboard/unified", headers=invalid_headers)
    assert response.status_code == 401

@pytest.mark.e2e
def test_tableau_bord_ml_performance(client: TestClient, test_user: dict):
    """Test des performances du tableau de bord ML"""
    # Authentification
    response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test du temps de réponse pour les données unifiées
    import time
    start_time = time.time()
    response = client.get("/api/v1/dashboard/unified", headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 2.0  # La réponse doit être < 2 secondes

    # Test du cache
    start_time = time.time()
    response = client.get("/api/v1/dashboard/unified", headers=headers)
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 0.5  # La réponse du cache doit être < 500ms

@pytest.mark.e2e
def test_tableau_bord_ml_websocket(client: TestClient, test_user: dict):
    """Test des mises à jour en temps réel du tableau de bord ML via WebSocket"""
    import websockets
    import json
    import asyncio

    async def websocket_test():
        # Authentification
        response = client.post("/api/v1/auth/login", json={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        token = response.json()["access_token"]

        # Connexion WebSocket
        async with websockets.connect(
            f"ws://localhost:8000/ws/dashboard?token={token}"
        ) as websocket:
            # Test des mises à jour en temps réel
            await websocket.send(json.dumps({
                "action": "subscribe",
                "modules": ["production", "finance"]
            }))

            # Attente de la confirmation d'abonnement
            response = await websocket.recv()
            response_data = json.loads(response)
            assert response_data["type"] == "subscription_confirmed"

            # Attente des mises à jour
            for _ in range(3):  # Attente de 3 mises à jour
                response = await websocket.recv()
                data = json.loads(response)
                assert "type" in data
                assert data["type"] in ["alert", "prediction", "update"]
                assert "module" in data
                assert "data" in data

    # Exécution du test WebSocket
    asyncio.get_event_loop().run_until_complete(websocket_test())
