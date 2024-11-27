import pytest
import time
from unittest.mock import Mock
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import psutil
import os
import concurrent.futures
import asyncio

from services.hr_analytics_service import HRAnalyticsService
from models.hr import Employee
from models.hr_formation import Formation, Participation
from models.hr_contract import Contract
from models.hr_payroll import Payroll

@pytest.fixture
def mock_db_session():
    """Crée une session DB mockée avec un grand nombre d'enregistrements"""
    session = Mock()
    
    # Création de données de test
    employees = [Mock(id=i) for i in range(10000)]  # Augmenté à 10000
    formations = [Mock(id=i, type=f"type_{i%5}") for i in range(1000)]  # Augmenté à 1000
    participations = [
        Mock(
            id=i,
            formation_id=i%1000,
            status='completed' if i%3==0 else 'in_progress',
            employee_id=i%10000
        ) for i in range(50000)  # Augmenté à 50000
    ]
    contracts = [
        Mock(
            id=i,
            employee_id=i%10000,
            type=f"type_{i%3}",
            start_date=datetime.now() - timedelta(days=i%365),
            end_date=datetime.now() + timedelta(days=i%365) if i%4!=0 else None,
            is_renewal=i%5==0
        ) for i in range(20000)  # Augmenté à 20000
    ]
    payrolls = [
        Mock(
            id=i,
            employee_id=i%10000,
            total_amount=float(3000 + (i%1000)),
            date=datetime.now() - timedelta(days=i%365),
            performance_rating=float(i%5 + 1)
        ) for i in range(100000)  # Augmenté à 100000
    ]
    
    # Configuration des retours des requêtes
    def query_side_effect(model):
        if model == Employee:
            return Mock(count=lambda: len(employees), all=lambda: employees)
        elif model == Formation:
            return Mock(all=lambda: formations)
        elif model == Participation:
            return Mock(
                all=lambda: participations,
                filter=lambda *args: Mock(all=lambda: [p for p in participations if p.employee_id == 1])
            )
        elif model == Contract:
            return Mock(
                all=lambda: contracts,
                filter=lambda *args: Mock(
                    count=lambda: len([c for c in contracts if c.status == 'active']),
                    all=lambda: [c for c in contracts if c.employee_id == 1]
                )
            )
        elif model == Payroll:
            return Mock(
                all=lambda: payrolls,
                filter=lambda *args: Mock(all=lambda: [p for p in payrolls if p.employee_id == 1])
            )
    
    session.query = Mock(side_effect=query_side_effect)
    return session

@pytest.fixture
def analytics_service(mock_db_session):
    """Crée une instance du service avec la session mockée"""
    return HRAnalyticsService(db=mock_db_session)

# Tests de performance de base
def test_get_employee_stats_performance(analytics_service, benchmark):
    """Test de performance pour get_employee_stats"""
    benchmark(analytics_service.get_employee_stats)

def test_get_formation_analytics_performance(analytics_service, benchmark):
    """Test de performance pour get_formation_analytics"""
    benchmark(analytics_service.get_formation_analytics)

def test_get_contract_analytics_performance(analytics_service, benchmark):
    """Test de performance pour get_contract_analytics"""
    benchmark(analytics_service.get_contract_analytics)

def test_get_payroll_analytics_performance(analytics_service, benchmark):
    """Test de performance pour get_payroll_analytics"""
    benchmark(analytics_service.get_payroll_analytics)

def test_predict_employee_performance_performance(analytics_service, benchmark):
    """Test de performance pour predict_employee_performance"""
    benchmark(lambda: analytics_service.predict_employee_performance(1))

# Tests de scalabilité
@pytest.mark.parametrize("num_records", [1000, 10000, 100000])
def test_get_employee_stats_scalability(mock_db_session, benchmark, num_records):
    """Test de scalabilité pour get_employee_stats avec différentes tailles de données"""
    employees = [Mock(id=i) for i in range(num_records)]
    mock_db_session.query(Employee).count.return_value = len(employees)
    
    service = HRAnalyticsService(db=mock_db_session)
    benchmark(service.get_employee_stats)

@pytest.mark.parametrize("num_records", [1000, 10000, 100000])
def test_get_formation_analytics_scalability(mock_db_session, benchmark, num_records):
    """Test de scalabilité pour get_formation_analytics avec différentes tailles de données"""
    formations = [Mock(id=i, type=f"type_{i%5}") for i in range(num_records)]
    participations = [
        Mock(
            id=i,
            formation_id=i%num_records,
            status='completed' if i%3==0 else 'in_progress'
        ) for i in range(num_records * 5)
    ]
    
    def query_side_effect(model):
        if model == Formation:
            return Mock(all=lambda: formations)
        elif model == Participation:
            return Mock(all=lambda: participations)
    
    mock_db_session.query = Mock(side_effect=query_side_effect)
    service = HRAnalyticsService(db=mock_db_session)
    benchmark(service.get_formation_analytics)

# Tests de charge
@pytest.mark.slow
def test_high_load_employee_stats(analytics_service):
    """Test de charge pour get_employee_stats avec un grand nombre de requêtes"""
    start_time = time.time()
    num_requests = 10000  # Augmenté à 10000
    
    for _ in range(num_requests):
        analytics_service.get_employee_stats()
    
    total_time = time.time() - start_time
    avg_time = total_time / num_requests
    
    assert avg_time < 0.1, f"Temps moyen par requête trop élevé: {avg_time}s"

@pytest.mark.slow
def test_high_load_formation_analytics(analytics_service):
    """Test de charge pour get_formation_analytics avec un grand nombre de requêtes"""
    start_time = time.time()
    num_requests = 10000  # Augmenté à 10000
    
    for _ in range(num_requests):
        analytics_service.get_formation_analytics()
    
    total_time = time.time() - start_time
    avg_time = total_time / num_requests
    
    assert avg_time < 0.1, f"Temps moyen par requête trop élevé: {avg_time}s"

# Tests de concurrence
def test_high_concurrency_requests(analytics_service):
    """Test de performance pour les requêtes hautement concurrentes"""
    import concurrent.futures
    import time
    
    def timed_request(func):
        start = time.time()
        result = func()
        return time.time() - start
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:  # Augmenté à 50 workers
        # Création de 50 requêtes concurrentes pour chaque endpoint
        futures = []
        for _ in range(50):  # Augmenté à 50 requêtes par endpoint
            futures.extend([
                executor.submit(timed_request, analytics_service.get_employee_stats),
                executor.submit(timed_request, analytics_service.get_formation_analytics),
                executor.submit(timed_request, analytics_service.get_contract_analytics),
                executor.submit(timed_request, analytics_service.get_payroll_analytics),
                executor.submit(lambda: timed_request(
                    lambda: analytics_service.predict_employee_performance(1)
                ))
            ])
        
        # Récupération des temps d'exécution
        times = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Vérification des performances
        avg_time = np.mean(times)
        max_time = np.max(times)
        p95_time = np.percentile(times, 95)
        
        assert avg_time < 0.5, f"Temps moyen d'exécution trop élevé: {avg_time}s"
        assert max_time < 1.0, f"Temps maximum d'exécution trop élevé: {max_time}s"
        assert p95_time < 0.75, f"95e percentile trop élevé: {p95_time}s"

# Tests de cache
def test_cache_effectiveness_high_load(analytics_service, benchmark):
    """Test de l'efficacité du cache sous forte charge"""
    # Premier appel (sans cache)
    first_call = benchmark(analytics_service.get_employee_stats)
    
    # Appels suivants (avec cache)
    times = []
    for _ in range(1000):  # Test avec 1000 appels consécutifs
        start = time.time()
        analytics_service.get_employee_stats()
        times.append(time.time() - start)
    
    avg_cached_time = np.mean(times)
    assert avg_cached_time < first_call.stats.stats.mean * 0.1, "Cache inefficace"

def test_cache_memory_usage(analytics_service):
    """Test de l'utilisation mémoire du cache sous forte charge"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Génération de charge sur le cache
    for _ in range(1000):
        analytics_service.get_employee_stats()
        analytics_service.get_formation_analytics()
        analytics_service.get_contract_analytics()
        analytics_service.get_payroll_analytics()
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # En MB
    
    assert memory_increase < 200, f"Augmentation mémoire trop importante: {memory_increase}MB"

# Tests de performance globaux
@pytest.mark.slow
def test_overall_system_performance(analytics_service):
    """Test de performance global du système"""
    start_time = time.time()
    
    # Test de charge
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(100):
            futures.extend([
                executor.submit(analytics_service.get_employee_stats),
                executor.submit(analytics_service.get_formation_analytics),
                executor.submit(analytics_service.get_contract_analytics),
                executor.submit(analytics_service.get_payroll_analytics),
                executor.submit(lambda: analytics_service.predict_employee_performance(1))
            ])
        
        # Attente de la fin des requêtes
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
