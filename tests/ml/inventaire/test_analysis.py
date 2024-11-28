"""
Tests pour le module d'analyse des stocks
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.ml.inventaire.analysis import StockAnalyzer

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
    """Fixture pour des mouvements de test avec patterns"""
    base_date = datetime.now(datetime.timezone.utc)
    mouvements = []
    
    # Création de patterns saisonniers
    for i in range(90):  # 3 mois de données
        # Plus de mouvements en début de mois
        quantite = 15.0 if i % 30 < 10 else 10.0
        # Alternance entrées/sorties
        type_mouvement = "ENTREE" if i % 2 == 0 else "SORTIE"
        
        mouvement = MouvementStock(
            id=f"mvt-{i}",
            produit_id="test-stock-1",
            type_mouvement=type_mouvement,
            quantite=quantite,
            date_mouvement=base_date - timedelta(days=i),
            cout_unitaire=10.0
        )
        mouvements.append(mouvement)
    
    return mouvements

def test_analyzer_initialization():
    """Test l'initialisation de l'analyseur"""
    analyzer = StockAnalyzer()
    assert not analyzer.is_trained
    assert analyzer.scaler is not None
    assert analyzer.cluster_model is not None

def test_prepare_dataframe(mock_stock, mock_mouvements):
    """Test la préparation du DataFrame"""
    analyzer = StockAnalyzer()
    df = analyzer._prepare_dataframe(mock_stock, mock_mouvements, 90)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "quantite" in df.columns
    assert "stock_cumule" in df.columns
    assert "cout" in df.columns

def test_analyze_trend(mock_stock, mock_mouvements):
    """Test l'analyse des tendances"""
    analyzer = StockAnalyzer()
    df = analyzer._prepare_dataframe(mock_stock, mock_mouvements, 90)
    trend = analyzer._analyze_trend(df)
    
    assert isinstance(trend, dict)
    assert "direction" in trend
    assert "force" in trend
    assert trend["direction"] in ["hausse", "baisse", "stable"]
    assert isinstance(trend["force"], float)
    assert 0 <= trend["force"] <= 1

def test_analyze_seasonality(mock_stock, mock_mouvements):
    """Test l'analyse de la saisonnalité"""
    analyzer = StockAnalyzer()
    df = analyzer._prepare_dataframe(mock_stock, mock_mouvements, 90)
    seasonality = analyzer._analyze_seasonality(df)
    
    assert isinstance(seasonality, dict)
    assert "patterns_semaine" in seasonality
    assert "patterns_mois" in seasonality
    
    # Vérification des patterns hebdomadaires
    assert len(seasonality["patterns_semaine"]) == 7
    for jour, valeur in seasonality["patterns_semaine"].items():
        assert isinstance(jour, str)
        assert isinstance(valeur, float)
    
    # Vérification des patterns mensuels
    assert len(seasonality["patterns_mois"]) <= 12
    for mois, valeur in seasonality["patterns_mois"].items():
        assert isinstance(mois, str)
        assert isinstance(valeur, float)

def test_detect_anomalies(mock_stock, mock_mouvements):
    """Test la détection des anomalies"""
    analyzer = StockAnalyzer()
    df = analyzer._prepare_dataframe(mock_stock, mock_mouvements, 90)
    anomalies = analyzer._detect_anomalies(df)
    
    assert isinstance(anomalies, list)
    for anomalie in anomalies:
        assert isinstance(anomalie, dict)
        assert "date" in anomalie
        assert "valeur" in anomalie
        assert "type" in anomalie
        assert "description" in anomalie

def test_generate_recommendations(mock_stock, mock_mouvements):
    """Test la génération des recommandations"""
    analyzer = StockAnalyzer()
    df = analyzer._prepare_dataframe(mock_stock, mock_mouvements, 90)
    
    trend = analyzer._analyze_trend(df)
    seasonality = analyzer._analyze_seasonality(df)
    anomalies = analyzer._detect_anomalies(df)
    
    recommendations = analyzer._generate_recommendations(
        mock_stock, trend, seasonality, anomalies
    )
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for rec in recommendations:
        assert isinstance(rec, str)

def test_analyze_stock_patterns_without_data(mock_stock):
    """Test l'analyse sans données historiques"""
    analyzer = StockAnalyzer()
    result = analyzer.analyze_stock_patterns(mock_stock, [])
    
    assert isinstance(result, dict)
    assert result["tendance"] == "stable"
    assert result["saisonnalite"] is None
    assert isinstance(result["anomalies"], list)
    assert isinstance(result["recommendations"], list)
    assert "date_analyse" in result

def test_analyze_stock_patterns_with_data(mock_stock, mock_mouvements):
    """Test l'analyse complète avec données"""
    analyzer = StockAnalyzer()
    result = analyzer.analyze_stock_patterns(mock_stock, mock_mouvements)
    
    assert isinstance(result, dict)
    assert "tendance" in result
    assert "force_tendance" in result
    assert "saisonnalite" in result
    assert "anomalies" in result
    assert "recommendations" in result
    assert "date_analyse" in result
    
    assert isinstance(result["force_tendance"], float)
    assert 0 <= result["force_tendance"] <= 1

@patch('services.ml.inventaire.analysis.cache_result')
def test_cache_behavior(mock_cache, mock_stock, mock_mouvements):
    """Test le comportement du cache"""
    analyzer = StockAnalyzer()
    
    # Première analyse
    result1 = analyzer.analyze_stock_patterns(mock_stock, mock_mouvements)
    
    # Deuxième analyse (devrait utiliser le cache)
    result2 = analyzer.analyze_stock_patterns(mock_stock, mock_mouvements)
    
    assert result1["tendance"] == result2["tendance"]
    assert result1["force_tendance"] == result2["force_tendance"]

def test_training_and_clustering(mock_stock, mock_mouvements):
    """Test l'entraînement et le clustering"""
    analyzer = StockAnalyzer()
    
    # Création de données d'entraînement
    stocks = [mock_stock]
    mouvements = {"test-stock-1": mock_mouvements}
    
    # Entraînement
    analyzer.train(stocks, mouvements)
    assert analyzer.is_trained
    
    # Vérification du clustering
    features = []
    for stock in stocks:
        stock_mouvements = mouvements.get(stock.id, [])
        if stock_mouvements:
            avg_qty = np.mean([m.quantite for m in stock_mouvements])
            std_qty = np.std([m.quantite for m in stock_mouvements])
            freq = len(stock_mouvements) / 30
            features.append([avg_qty, std_qty, freq])
    
    if features:
        features = np.array(features)
        features_scaled = analyzer.scaler.transform(features)
        clusters = analyzer.cluster_model.predict(features_scaled)
        assert len(clusters) == len(features)
