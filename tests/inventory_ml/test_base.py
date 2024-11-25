"""
Tests pour le modèle ML de base de l'inventaire
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.inventory_ml.base import InventoryMLModel

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

def test_model_initialization():
    """Test l'initialisation du modèle"""
    model = InventoryMLModel()
    assert not model.is_trained
    assert model.model is not None
    assert model.scaler is not None

def test_prepare_features(mock_stock, mock_mouvements):
    """Test la préparation des features"""
    model = InventoryMLModel()
    features = model._prepare_features(mock_stock, mock_mouvements)
    
    assert isinstance(features, np.ndarray)
    assert features.shape == (1, 10)  # Vérifier la dimension des features

def test_predict_without_training(mock_stock, mock_mouvements):
    """Test la prédiction sans entraînement"""
    model = InventoryMLModel()
    
    with pytest.raises(ValueError, match="Le modèle doit être entraîné"):
        model.predict_stock_optimal(mock_stock, mock_mouvements)

def test_training_and_prediction(mock_stock, mock_mouvements):
    """Test l'entraînement et la prédiction"""
    model = InventoryMLModel()
    
    # Création de données d'entraînement
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    
    # Entraînement
    model.train(stocks, mouvements)
    assert model.is_trained
    
    # Prédiction
    prediction = model.predict_stock_optimal(mock_stock, mock_mouvements)
    
    assert isinstance(prediction, dict)
    assert "niveau_optimal" in prediction
    assert "confiance" in prediction
    assert "date_prediction" in prediction
    assert isinstance(prediction["niveau_optimal"], float)
    assert 0 <= prediction["confiance"] <= 1

def test_model_persistence(tmp_path, mock_stock, mock_mouvements):
    """Test la persistance du modèle"""
    model = InventoryMLModel()
    
    # Entraînement initial
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    model.train(stocks, mouvements)
    
    # Sauvegarde
    save_path = tmp_path / "test_model.joblib"
    model.save_model(str(save_path))
    assert save_path.exists()
    
    # Chargement dans un nouveau modèle
    new_model = InventoryMLModel()
    new_model.load_model(str(save_path))
    assert new_model.is_trained
    
    # Vérification des prédictions
    pred1 = model.predict_stock_optimal(mock_stock, mock_mouvements)
    pred2 = new_model.predict_stock_optimal(mock_stock, mock_mouvements)
    
    assert np.isclose(pred1["niveau_optimal"], pred2["niveau_optimal"], rtol=1e-10)
    assert np.isclose(pred1["confiance"], pred2["confiance"], rtol=1e-10)

def test_cache_behavior(mock_stock, mock_mouvements):
    """Test le comportement du cache"""
    model = InventoryMLModel()
    
    # Entraînement
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    model.train(stocks, mouvements)
    
    # Première prédiction
    pred1 = model.predict_stock_optimal(mock_stock, mock_mouvements)
    
    # Deuxième prédiction (devrait utiliser le cache)
    pred2 = model.predict_stock_optimal(mock_stock, mock_mouvements)
    
    assert pred1["niveau_optimal"] == pred2["niveau_optimal"]
    assert pred1["confiance"] == pred2["confiance"]

def test_error_handling():
    """Test la gestion des erreurs"""
    model = InventoryMLModel()
    
    # Test avec des données invalides
    with pytest.raises(ValueError):
        model.train([], {})
    
    with pytest.raises(ValueError):
        model.save_model("test.joblib")  # Modèle non entraîné
