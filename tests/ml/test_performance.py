"""
Tests de performance pour les fonctionnalités ML du tableau de bord.
"""

import pytest
import time
import asyncio
from datetime import datetime, timedelta
from services.ml.tableau_bord.unification import TableauBordUnifieService

@pytest.mark.performance
async def test_ml_predictions_performance(mock_ml_services):
    """Test des performances des prédictions ML"""
    # Configuration
    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Test de performance sans cache
    start_time = time.time()
    await unified_service.get_unified_dashboard_data()
    end_time = time.time()
    
    # La génération initiale des données doit prendre moins de 2 secondes
    assert end_time - start_time < 2.0

    # Test de performance avec cache
    mock_ml_services["cache"].get.return_value = {
        "timestamp": datetime.now().isoformat(),
        "data": {"test": "data"}
    }

    start_time = time.time()
    await unified_service.get_unified_dashboard_data()
    end_time = time.time()
    
    # L'accès au cache doit prendre moins de 100ms
    assert end_time - start_time < 0.1

@pytest.mark.performance
async def test_ml_concurrent_requests(mock_ml_services):
    """Test des performances avec des requêtes concurrentes"""
    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Simulation de 10 requêtes concurrentes
    async def make_request():
        return await unified_service.get_unified_dashboard_data()

    start_time = time.time()
    tasks = [make_request() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    end_time = time.time()

    # 10 requêtes concurrentes doivent prendre moins de 5 secondes
    assert end_time - start_time < 5.0
    assert len(results) == 10

@pytest.mark.performance
async def test_ml_cache_expiration(mock_ml_services, mock_ml_cache_data):
    """Test des performances avec expiration du cache"""
    # Configuration du cache avec des données expirées
    expired_data = mock_ml_cache_data.copy()
    expired_data["timestamp"] = (datetime.now() - timedelta(minutes=16)).isoformat()
    mock_ml_services["cache"].get.return_value = expired_data

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    start_time = time.time()
    await unified_service.get_unified_dashboard_data()
    end_time = time.time()

    # La régénération des données après expiration du cache doit prendre moins de 3 secondes
    assert end_time - start_time < 3.0

@pytest.mark.performance
async def test_ml_memory_usage(mock_ml_services):
    """Test de l'utilisation mémoire des fonctionnalités ML"""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Génération des données
    await unified_service.get_unified_dashboard_data()

    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory

    # L'augmentation de la mémoire ne doit pas dépasser 50MB
    assert memory_increase < 50 * 1024 * 1024  # 50MB en bytes

@pytest.mark.performance
async def test_ml_data_volume(mock_ml_services):
    """Test des performances avec un grand volume de données"""
    # Modification des mocks pour simuler un grand volume de données
    mock_ml_services["production"].get_daily_production.return_value = [
        {"timestamp": datetime.now() - timedelta(days=i), "value": i}
        for i in range(1000)  # 1000 points de données
    ]

    mock_ml_services["inventory"].get_total_items.return_value = {
        f"item_{i}": {"quantity": i, "value": i * 100}
        for i in range(1000)  # 1000 produits
    }

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    start_time = time.time()
    data = await unified_service.get_unified_dashboard_data()
    end_time = time.time()

    # Le traitement d'un grand volume de données doit prendre moins de 5 secondes
    assert end_time - start_time < 5.0
    
    # Vérification de la taille des données
    import sys
    data_size = sys.getsizeof(str(data))  # Estimation approximative
    assert data_size < 10 * 1024 * 1024  # Moins de 10MB
