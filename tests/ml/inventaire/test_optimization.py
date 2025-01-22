"""
Tests pour le module d'optimisation des stocks
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.ml.inventaire.optimization import OptimiseurStock

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
            "humidite": 50
        },
        conditions_actuelles={
            "temperature": 22,
            "humidite": 55
        }
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
            cout_unitaire=10.0
        )
        for i in range(10)
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

def test_optimizer_initialization():
    """Test l'initialisation de l'optimiseur"""
    optimizer = OptimiseurStock()
    assert not optimizer.is_trained
    assert optimizer.base_model is not None
    assert optimizer.optimizer is not None

def test_optimize_without_training(mock_stock, mock_mouvements, mock_weather_data):
    """Test l'optimisation sans entraînement"""
    optimizer = OptimiseurStock()
    
    with pytest.raises(ValueError, match="L'optimiseur doit être entraîné"):
        optimizer.optimize_stock_levels(mock_stock, mock_mouvements, mock_weather_data)

def test_training_and_optimization(mock_stock, mock_mouvements, mock_weather_data):
    """Test l'entraînement et l'optimisation"""
    optimizer = OptimiseurStock()
    
    # Création de données d'entraînement
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    
    # Entraînement
    optimizer.train(stocks, mouvements)
    assert optimizer.is_trained
    
    # Optimisation
    result = optimizer.optimize_stock_levels(mock_stock, mock_mouvements, mock_weather_data)
    
    assert isinstance(result, dict)
    assert "niveau_optimal" in result
    assert "niveau_min" in result
    assert "niveau_max" in result
    assert "ajustements" in result
    assert "confiance" in result
    assert "date_optimisation" in result

def test_seasonal_factor(mock_stock, mock_mouvements):
    """Test le calcul du facteur saisonnier"""
    optimizer = OptimiseurStock()
    factor = optimizer._seasonal_factor(mock_stock, mock_mouvements)
    
    assert isinstance(factor, float)
    assert 0.8 <= factor <= 1.2

def test_expiration_factor(mock_stock):
    """Test le calcul du facteur de péremption"""
    optimizer = OptimiseurStock()
    
    # Test avec date de péremption future
    mock_stock.date_peremption = datetime.now(datetime.timezone.utc) + timedelta(days=100)
    factor = optimizer._expiration_factor(mock_stock)
    assert factor == 1.0
    
    # Test avec date de péremption proche
    mock_stock.date_peremption = datetime.now(datetime.timezone.utc) + timedelta(days=20)
    factor = optimizer._expiration_factor(mock_stock)
    assert factor < 1.0
    
    # Test sans date de péremption
    mock_stock.date_peremption = None
    factor = optimizer._expiration_factor(mock_stock)
    assert factor == 1.0

def test_weather_factor(mock_stock, mock_weather_data):
    """Test le calcul du facteur météorologique"""
    optimizer = OptimiseurStock()
    
    # Test avec conditions optimales
    factor = optimizer._weather_factor(mock_stock, mock_weather_data)
    assert isinstance(factor, float)
    assert 0.8 <= factor <= 1.0
    
    # Test sans données météo
    factor = optimizer._weather_factor(mock_stock, None)
    assert factor == 1.0
    
    # Test sans conditions de stockage
    mock_stock.conditions_stockage = None
    factor = optimizer._weather_factor(mock_stock, mock_weather_data)
    assert factor == 1.0

def test_trend_factor(mock_mouvements):
    """Test le calcul du facteur de tendance"""
    optimizer = OptimiseurStock()
    
    # Test avec mouvements
    factor = optimizer._trend_factor(mock_mouvements)
    assert isinstance(factor, float)
    assert 0.8 <= factor <= 1.2
    
    # Test sans mouvements
    factor = optimizer._trend_factor([])
    assert factor == 1.0

def test_adjustments_calculation(mock_stock, mock_mouvements, mock_weather_data):
    """Test le calcul des ajustements"""
    optimizer = OptimiseurStock()
    adjustments = optimizer._calculate_adjustments(
        mock_stock, mock_mouvements, mock_weather_data
    )
    
    assert isinstance(adjustments, dict)
    assert "saisonnalite" in adjustments
    assert "peremption" in adjustments
    assert "meteo" in adjustments
    assert "tendance" in adjustments
    assert "facteur_global" in adjustments
    
    # Vérification des valeurs
    for factor in adjustments.values():
        assert isinstance(factor, float)
        assert 0.5 <= factor <= 1.5

@patch('services.cache_service.cache_result')
def test_cache_behavior(mock_cache, mock_stock, mock_mouvements, mock_weather_data):
    """Test le comportement du cache"""
    optimizer = OptimiseurStock()
    optimizer.train([mock_stock], {"test-stock-1": mock_mouvements})
    
    # Première optimisation
    result1 = optimizer.optimize_stock_levels(mock_stock, mock_mouvements, mock_weather_data)
    
    # Deuxième optimisation (devrait utiliser le cache)
    result2 = optimizer.optimize_stock_levels(mock_stock, mock_mouvements, mock_weather_data)
    
    assert result1["niveau_optimal"] == result2["niveau_optimal"]
    assert result1["ajustements"] == result2["ajustements"]

def test_error_handling():
    """Test la gestion des erreurs"""
    optimizer = OptimiseurStock()
    
    # Test avec des données invalides
    with pytest.raises(ValueError):
        optimizer.train([], {})
