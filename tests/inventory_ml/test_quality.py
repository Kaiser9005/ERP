"""
Tests pour le module de prédiction de qualité des stocks
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.inventory_ml.quality import QualityPredictor

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
        date_peremption=datetime.now(datetime.timezone.utc) + timedelta(days=60)
    )

@pytest.fixture
def mock_conditions_actuelles():
    """Fixture pour les conditions actuelles"""
    return {
        "temperature": 22,
        "humidite": 55,
        "ventilation": True
    }

@pytest.fixture
def mock_historique_conditions():
    """Fixture pour l'historique des conditions"""
    base_date = datetime.now(datetime.timezone.utc)
    return [
        {
            "date": (base_date - timedelta(hours=i)).isoformat(),
            "temperature": 20 + np.random.normal(0, 1),
            "humidite": 50 + np.random.normal(0, 2),
            "ventilation": True
        }
        for i in range(24 * 7)  # Une semaine de données
    ]

def test_predictor_initialization():
    """Test l'initialisation du prédicteur"""
    predictor = QualityPredictor()
    assert not predictor.is_trained
    assert predictor.model is not None
    assert predictor.scaler is not None

def test_prepare_features(mock_stock, mock_conditions_actuelles, mock_historique_conditions):
    """Test la préparation des features"""
    predictor = QualityPredictor()
    features = predictor._prepare_features(
        mock_stock,
        mock_conditions_actuelles,
        mock_historique_conditions
    )
    
    assert isinstance(features, np.ndarray)
    assert len(features) > 0

def test_predict_without_training(mock_stock, mock_conditions_actuelles, mock_historique_conditions):
    """Test la prédiction sans entraînement"""
    predictor = QualityPredictor()
    
    with pytest.raises(ValueError, match="Le modèle doit être entraîné"):
        predictor.predict_quality_risk(
            mock_stock,
            mock_conditions_actuelles,
            mock_historique_conditions
        )

def test_training_and_prediction(mock_stock, mock_conditions_actuelles, mock_historique_conditions):
    """Test l'entraînement et la prédiction"""
    predictor = QualityPredictor()
    
    # Création de données d'entraînement
    stocks = [mock_stock]
    conditions_historiques = {
        "test-stock-1": mock_historique_conditions
    }
    quality_labels = {
        "test-stock-1": 1  # Bonne qualité
    }
    
    # Entraînement
    predictor.train(stocks, conditions_historiques, quality_labels)
    assert predictor.is_trained
    
    # Prédiction
    prediction = predictor.predict_quality_risk(
        mock_stock,
        mock_conditions_actuelles,
        mock_historique_conditions
    )
    
    assert isinstance(prediction, dict)
    assert "niveau_risque" in prediction
    assert prediction["niveau_risque"] in ["faible", "moyen", "élevé"]
    assert "probabilite" in prediction
    assert 0 <= prediction["probabilite"] <= 1
    assert "facteurs_risque" in prediction
    assert "recommendations" in prediction
    assert "date_prediction" in prediction

def test_calculate_risk_level():
    """Test le calcul du niveau de risque"""
    predictor = QualityPredictor()
    
    # Test différents niveaux de probabilité
    assert predictor._calculate_risk_level(np.array([0.8, 0.2])) == "élevé"
    assert predictor._calculate_risk_level(np.array([0.5, 0.5])) == "moyen"
    assert predictor._calculate_risk_level(np.array([0.2, 0.8])) == "faible"

def test_analyze_risk_factors(mock_stock, mock_conditions_actuelles, mock_historique_conditions):
    """Test l'analyse des facteurs de risque"""
    predictor = QualityPredictor()
    risk_factors = predictor._analyze_risk_factors(
        mock_stock,
        mock_conditions_actuelles,
        mock_historique_conditions
    )
    
    assert isinstance(risk_factors, list)
    for factor in risk_factors:
        assert isinstance(factor, dict)
        assert "type" in factor
        assert "severite" in factor
        assert "description" in factor
        assert factor["severite"] in ["élevée", "moyenne"]

def test_generate_recommendations():
    """Test la génération des recommandations"""
    predictor = QualityPredictor()
    
    # Test avec risque élevé
    risk_factors_high = [
        {
            "type": "temperature",
            "severite": "élevée",
            "description": "Écart de température important"
        }
    ]
    recommendations_high = predictor._generate_recommendations("élevé", risk_factors_high)
    assert len(recommendations_high) > 0
    assert "Inspection immédiate" in recommendations_high[0]
    
    # Test avec risque faible
    risk_factors_low = []
    recommendations_low = predictor._generate_recommendations("faible", risk_factors_low)
    assert len(recommendations_low) > 0
    assert "surveillance régulière" in recommendations_low[0].lower()

@patch('services.inventory_ml.quality.cache_result')
def test_cache_behavior(mock_cache, mock_stock, mock_conditions_actuelles, mock_historique_conditions):
    """Test le comportement du cache"""
    predictor = QualityPredictor()
    
    # Entraînement
    stocks = [mock_stock]
    conditions_historiques = {"test-stock-1": mock_historique_conditions}
    quality_labels = {"test-stock-1": 1}
    predictor.train(stocks, conditions_historiques, quality_labels)
    
    # Première prédiction
    result1 = predictor.predict_quality_risk(
        mock_stock,
        mock_conditions_actuelles,
        mock_historique_conditions
    )
    
    # Deuxième prédiction (devrait utiliser le cache)
    result2 = predictor.predict_quality_risk(
        mock_stock,
        mock_conditions_actuelles,
        mock_historique_conditions
    )
    
    assert result1["niveau_risque"] == result2["niveau_risque"]
    assert result1["probabilite"] == result2["probabilite"]

def test_error_handling():
    """Test la gestion des erreurs"""
    predictor = QualityPredictor()
    
    # Test avec des données invalides
    with pytest.raises(ValueError):
        predictor.train([], {}, {})

def test_with_missing_conditions(mock_stock):
    """Test avec des conditions manquantes"""
    predictor = QualityPredictor()
    
    # Test sans conditions actuelles
    mock_stock.conditions_actuelles = None
    mock_stock.conditions_stockage = None
    
    # Entraînement minimal
    predictor.train([mock_stock], {"test-stock-1": []}, {"test-stock-1": 0})
    
    # La prédiction devrait fonctionner même sans conditions
    result = predictor.predict_quality_risk(mock_stock, {}, [])
    
    assert isinstance(result, dict)
    assert "niveau_risque" in result
    assert "recommendations" in result
