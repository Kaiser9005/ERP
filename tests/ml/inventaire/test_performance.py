"""
Tests de performance pour les fonctionnalités ML d'inventaire
"""

import pytest
import time
import numpy as np
from datetime import datetime, timedelta
import psutil
import os
import concurrent.futures
import asyncio
from unittest.mock import Mock

from models.inventory import Stock, MouvementStock, CategoryProduit, UniteMesure
from services.ml.inventaire.optimization import OptimiseurStock
from services.ml.inventaire.analysis import AnalyseurStock
from services.ml.inventaire.quality import PredicteurQualite
from services.ml.inventaire import InventoryMLService

@pytest.fixture
def mock_db_session():
    """Crée une session DB mockée avec un grand nombre d'enregistrements"""
    session = Mock()
    
    # Création de données de test
    stocks = [
        Stock(
            id=f"stock-{i}",
            code=f"TEST{i:04d}",
            nom=f"Test Produit {i}",
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
        for i in range(10000)  # 10000 stocks
    ]
    
    mouvements = {}
    base_date = datetime.now(datetime.timezone.utc)
    for stock in stocks:
        mouvements[stock.id] = [
            MouvementStock(
                id=f"mvt-{stock.id}-{j}",
                produit_id=stock.id,
                type_mouvement="ENTREE" if j % 2 == 0 else "SORTIE",
                quantite=10.0,
                date_mouvement=base_date - timedelta(days=j),
                cout_unitaire=10.0
            )
            for j in range(365)  # Un an de mouvements par stock
        ]
    
    def query_side_effect(model):
        if model == Stock:
            return Mock(all=lambda: stocks)
        elif model == MouvementStock:
            return Mock(
                filter=lambda *args: Mock(all=lambda: mouvements.get(args[0].id, []))
            )
    
    session.query = Mock(side_effect=query_side_effect)
    return session

@pytest.fixture
def ml_service(mock_db_session):
    """Crée une instance du service ML avec la session mockée"""
    return InventoryMLService(db=mock_db_session)

# Tests de performance de base
def test_optimizer_performance(ml_service, benchmark):
    """Test de performance pour l'optimiseur de stock"""
    benchmark(ml_service.optimizer.optimize_stock_levels)

def test_analyzer_performance(ml_service, benchmark):
    """Test de performance pour l'analyseur de stock"""
    benchmark(ml_service.analyzer.analyze_stock_patterns)

def test_quality_predictor_performance(ml_service, benchmark):
    """Test de performance pour le prédicteur de qualité"""
    benchmark(ml_service.quality_predictor.predict_quality_risk)

# Tests de scalabilité
@pytest.mark.parametrize("num_records", [1000, 10000, 100000])
def test_optimizer_scalability(mock_db_session, benchmark, num_records):
    """Test de scalabilité pour l'optimiseur avec différentes tailles de données"""
    stocks = [
        Stock(
            id=f"stock-{i}",
            code=f"TEST{i:04d}",
            nom=f"Test Produit {i}",
            categorie=CategoryProduit.INTRANT,
            unite_mesure=UniteMesure.KG,
            quantite=100.0,
            prix_unitaire=10.0,
            seuil_alerte=20.0
        )
        for i in range(num_records)
    ]
    
    optimizer = OptimiseurStock()
    benchmark(optimizer.train, stocks, {})

@pytest.mark.parametrize("num_records", [1000, 10000, 100000])
def test_analyzer_scalability(mock_db_session, benchmark, num_records):
    """Test de scalabilité pour l'analyseur avec différentes tailles de données"""
    stocks = [
        Stock(
            id=f"stock-{i}",
            code=f"TEST{i:04d}",
            nom=f"Test Produit {i}",
            categorie=CategoryProduit.INTRANT,
            unite_mesure=UniteMesure.KG,
            quantite=100.0,
            prix_unitaire=10.0,
            seuil_alerte=20.0
        )
        for i in range(num_records)
    ]
    
    analyzer = AnalyseurStock()
    benchmark(analyzer.train, stocks, {})

# Tests de charge
@pytest.mark.slow
def test_high_load_optimizer(ml_service):
    """Test de charge pour l'optimiseur avec un grand nombre de requêtes"""
    start_time = time.time()
    num_requests = 10000
    
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    for _ in range(num_requests):
        ml_service.optimizer.optimize_stock_levels(stock, [])
    
    total_time = time.time() - start_time
    avg_time = total_time / num_requests
    
    assert avg_time < 0.1, f"Temps moyen par requête trop élevé: {avg_time}s"

@pytest.mark.slow
def test_high_load_analyzer(ml_service):
    """Test de charge pour l'analyseur avec un grand nombre de requêtes"""
    start_time = time.time()
    num_requests = 10000
    
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    for _ in range(num_requests):
        ml_service.analyzer.analyze_stock_patterns(stock, [])
    
    total_time = time.time() - start_time
    avg_time = total_time / num_requests
    
    assert avg_time < 0.1, f"Temps moyen par requête trop élevé: {avg_time}s"

# Tests de concurrence
def test_high_concurrency_requests(ml_service):
    """Test de performance pour les requêtes hautement concurrentes"""
    def timed_request(func):
        start = time.time()
        result = func()
        return time.time() - start
    
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for _ in range(50):
            futures.extend([
                executor.submit(lambda: timed_request(
                    lambda: ml_service.optimizer.optimize_stock_levels(stock, [])
                )),
                executor.submit(lambda: timed_request(
                    lambda: ml_service.analyzer.analyze_stock_patterns(stock, [])
                )),
                executor.submit(lambda: timed_request(
                    lambda: ml_service.quality_predictor.predict_quality_risk(
                        stock, {}, []
                    )
                ))
            ])
        
        times = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        avg_time = np.mean(times)
        max_time = np.max(times)
        p95_time = np.percentile(times, 95)
        
        assert avg_time < 0.5, f"Temps moyen d'exécution trop élevé: {avg_time}s"
        assert max_time < 1.0, f"Temps maximum d'exécution trop élevé: {max_time}s"
        assert p95_time < 0.75, f"95e percentile trop élevé: {p95_time}s"

# Tests de cache
def test_cache_effectiveness_high_load(ml_service, benchmark):
    """Test de l'efficacité du cache sous forte charge"""
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    # Premier appel (sans cache)
    first_call = benchmark(ml_service.get_stock_insights, stock, [])
    
    # Appels suivants (avec cache)
    times = []
    for _ in range(1000):
        start = time.time()
        ml_service.get_stock_insights(stock, [])
        times.append(time.time() - start)
    
    avg_cached_time = np.mean(times)
    assert avg_cached_time < first_call.stats.stats.mean * 0.1, "Cache inefficace"

def test_cache_memory_usage(ml_service):
    """Test de l'utilisation mémoire du cache sous forte charge"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    # Génération de charge sur le cache
    for _ in range(1000):
        ml_service.get_stock_insights(stock, [])
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # En MB
    
    assert memory_increase < 200, f"Augmentation mémoire trop importante: {memory_increase}MB"

# Tests de performance globaux
@pytest.mark.slow
def test_overall_system_performance(ml_service):
    """Test de performance global du système"""
    start_time = time.time()
    
    stock = Stock(
        id="test-stock",
        code="TEST001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        quantite=100.0,
        prix_unitaire=10.0,
        seuil_alerte=20.0
    )
    
    # Test de charge
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(100):
            futures.extend([
                executor.submit(lambda: ml_service.get_stock_insights(stock, [])),
                executor.submit(lambda: ml_service.optimizer.optimize_stock_levels(stock, [])),
                executor.submit(lambda: ml_service.analyzer.analyze_stock_patterns(stock, [])),
                executor.submit(lambda: ml_service.quality_predictor.predict_quality_risk(stock, {}, []))
            ])
        
        concurrent.futures.wait(futures)
    
    total_time = time.time() - start_time
    
    # Vérification des métriques
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # En MB
    cpu_percent = process.cpu_percent()
    
    assert total_time < 30, f"Temps total d'exécution trop élevé: {total_time}s"
    assert memory_usage < 500, f"Utilisation mémoire trop élevée: {memory_usage}MB"
    assert cpu_percent < 80, f"Utilisation CPU trop élevée: {cpu_percent}%"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
