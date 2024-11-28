"""
Tests d'intégration pour le service ML d'inventaire
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.ml.inventaire import InventoryMLService
from services.weather_service import WeatherService
from services.iot_service import IoTService

@pytest.fixture
def mock_stock():
    """Fixture pour un stock de test"""
    return Stock(
        id="test-stock-1",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0,
        conditions_stockage={
            "temperature": 20,
            "humidite": 50,
            "ventilation": True
        },
        conditions_actuelles={
            "temperature": 22,
            "humidite": 55,
            "ventilation": True
        },
        date_peremption=datetime.now(datetime.timezone.utc) + timedelta(days=60),
        capteurs_id=["sensor-1", "sensor-2"]
    )

@pytest.fixture
def mock_mouvements():
    """Fixture pour des mouvements de test"""
    base_date = datetime.now(datetime.timezone.utc)
    return [
        MouvementStock(
            id=f"mvt-{i}",
            produit_id="test-stock-1",
            type_mouvement="ENTREE" if i % 2 == 0 else "SORTIE",
            quantite=10.0,
            date_mouvement=base_date - timedelta(days=i),
            cout_unitaire=10.0,
            conditions_transport={
                "temperature": 21,
                "humidite": 52
            }
        )
        for i in range(30)
    ]

@pytest.fixture
def mock_weather_data():
    """Fixture pour les données météo"""
    return {
        "temperature": 21.5,
        "humidite": 52,
        "pression": 1013,
        "precipitation": 0,
        "vent": 5
    }

@pytest.fixture
def mock_iot_data():
    """Fixture pour les données IoT"""
    return {
        "temperature": 21.8,
        "humidite": 53,
        "ventilation": True,
        "timestamp": datetime.now(datetime.timezone.utc).isoformat()
    }

@pytest.fixture
def mock_historical_iot_data():
    """Fixture pour l'historique des données IoT"""
    base_date = datetime.now(datetime.timezone.utc)
    return [
        {
            "temperature": 20 + (i % 3),
            "humidite": 50 + (i % 5),
            "ventilation": True,
            "timestamp": (base_date - timedelta(hours=i)).isoformat()
        }
        for i in range(24 * 7)  # Une semaine de données
    ]

@pytest.fixture
def service():
    """Fixture pour le service ML"""
    return InventoryMLService()

def test_service_initialization(service):
    """Test l'initialisation du service"""
    assert service.base_model is not None
    assert service.optimizer is not None
    assert service.analyzer is not None
    assert service.quality_predictor is not None
    assert not service.is_trained

@patch.object(WeatherService, 'get_current_conditions')
@patch.object(IoTService, 'get_sensor_data')
@patch.object(IoTService, 'get_historical_data')
def test_get_stock_insights_without_training(
    mock_get_historical,
    mock_get_sensor,
    mock_get_weather,
    service,
    mock_stock,
    mock_mouvements,
    mock_weather_data,
    mock_iot_data,
    mock_historical_iot_data
):
    """Test l'obtention des insights sans entraînement"""
    with pytest.raises(ValueError, match="Le service ML doit être entraîné"):
        service.get_stock_insights(mock_stock, mock_mouvements)

@patch.object(WeatherService, 'get_current_conditions')
@patch.object(IoTService, 'get_sensor_data')
@patch.object(IoTService, 'get_historical_data')
def test_get_stock_insights_with_training(
    mock_get_historical,
    mock_get_sensor,
    mock_get_weather,
    service,
    mock_stock,
    mock_mouvements,
    mock_weather_data,
    mock_iot_data,
    mock_historical_iot_data
):
    """Test l'obtention des insights après entraînement"""
    # Configuration des mocks
    mock_get_weather.return_value = mock_weather_data
    mock_get_sensor.return_value = mock_iot_data
    mock_get_historical.return_value = mock_historical_iot_data
    
    # Entraînement du service
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    conditions_historiques = {"test-stock-1": mock_historical_iot_data}
    quality_labels = {"test-stock-1": 1}
    
    service.train(stocks, mouvements, conditions_historiques, quality_labels)
    assert service.is_trained
    
    # Test des insights
    insights = service.get_stock_insights(mock_stock, mock_mouvements)
    
    assert isinstance(insights, dict)
    assert "niveau_optimal" in insights
    assert "optimisation" in insights
    assert "patterns" in insights
    assert "risque_qualite" in insights
    assert "date_analyse" in insights
    assert "meteo" in insights
    assert "donnees_iot" in insights

def test_model_persistence(service, mock_stock, mock_mouvements, tmp_path):
    """Test la persistance des modèles"""
    # Entraînement initial
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    service.train(stocks, mouvements)
    
    # Sauvegarde
    base_path = tmp_path / "models"
    base_path.mkdir()
    service.save_models(str(base_path))
    
    # Nouveau service
    new_service = InventoryMLService()
    new_service.load_models(str(base_path))
    
    assert new_service.is_trained
    assert new_service.base_model.is_trained
    assert new_service.optimizer.is_trained
    assert new_service.analyzer.is_trained
    assert new_service.quality_predictor.is_trained

@patch.object(WeatherService, 'get_current_conditions')
@patch.object(IoTService, 'get_sensor_data')
@patch.object(IoTService, 'get_historical_data')
def test_error_handling(
    mock_get_historical,
    mock_get_sensor,
    mock_get_weather,
    service,
    mock_stock,
    mock_mouvements
):
    """Test la gestion des erreurs"""
    # Test avec erreur météo
    mock_get_weather.side_effect = Exception("Erreur météo")
    mock_get_sensor.return_value = None
    mock_get_historical.return_value = []
    
    service.train([mock_stock], {"test-stock-1": mock_mouvements})
    
    # Le service devrait continuer à fonctionner même sans données externes
    insights = service.get_stock_insights(mock_stock, mock_mouvements)
    assert isinstance(insights, dict)
    assert insights["meteo"] is None

@patch.object(WeatherService, 'get_current_conditions')
@patch.object(IoTService, 'get_sensor_data')
@patch.object(IoTService, 'get_historical_data')
def test_cache_behavior(
    mock_get_historical,
    mock_get_sensor,
    mock_get_weather,
    service,
    mock_stock,
    mock_mouvements,
    mock_weather_data,
    mock_iot_data,
    mock_historical_iot_data
):
    """Test le comportement du cache"""
    # Configuration des mocks
    mock_get_weather.return_value = mock_weather_data
    mock_get_sensor.return_value = mock_iot_data
    mock_get_historical.return_value = mock_historical_iot_data
    
    # Entraînement
    service.train([mock_stock], {"test-stock-1": mock_mouvements})
    
    # Première requête
    insights1 = service.get_stock_insights(mock_stock, mock_mouvements)
    
    # Deuxième requête (devrait utiliser le cache)
    insights2 = service.get_stock_insights(mock_stock, mock_mouvements)
    
    assert insights1["niveau_optimal"] == insights2["niveau_optimal"]
    assert insights1["optimisation"] == insights2["optimisation"]
    assert insights1["patterns"] == insights2["patterns"]
    
    # Vérification que les services externes n'ont été appelés qu'une fois
    mock_get_weather.assert_called_once()
    mock_get_sensor.assert_called_once()
    mock_get_historical.assert_called_once()
