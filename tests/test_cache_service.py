"""Tests pour le service de cache."""

import pytest
from datetime import timedelta
import asyncio
from services.cache_service import CacheService, cache_result, get_cache_service

@pytest.fixture
async def cache_service():
    """Fixture pour le service de cache"""
    service = CacheService()
    await service.clear()  # S'assurer que le cache est vide
    return service

@pytest.mark.asyncio
async def test_basic_cache_operations(cache_service):
    """Test des opérations basiques du cache"""
    # Test set/get
    await cache_service.set("test_key", "test_value")
    value = await cache_service.get("test_key")
    assert value == "test_value"
    
    # Test expiration
    await cache_service.set("expire_key", "expire_value", timedelta(seconds=1))
    value = await cache_service.get("expire_key")
    assert value == "expire_value"
    
    await asyncio.sleep(1.1)  # Attendre l'expiration
    value = await cache_service.get("expire_key")
    assert value is None
    
    # Test invalidation
    await cache_service.set("invalid_key", "invalid_value")
    await cache_service.invalidate("invalid_key")
    value = await cache_service.get("invalid_key")
    assert value is None
    
    # Test clear
    await cache_service.set("clear_key", "clear_value")
    await cache_service.clear()
    value = await cache_service.get("clear_key")
    assert value is None

@pytest.mark.asyncio
async def test_get_or_compute(cache_service):
    """Test de la méthode get_or_compute"""
    compute_count = 0
    
    async def compute_value():
        nonlocal compute_count
        compute_count += 1
        return f"computed_{compute_count}"
    
    # Premier appel - devrait calculer
    value = await cache_service.get_or_compute(
        "compute_key",
        compute_value,
        timedelta(seconds=1)
    )
    assert value == "computed_1"
    assert compute_count == 1
    
    # Deuxième appel - devrait utiliser le cache
    value = await cache_service.get_or_compute(
        "compute_key",
        compute_value,
        timedelta(seconds=1)
    )
    assert value == "computed_1"
    assert compute_count == 1
    
    # Attendre l'expiration
    await asyncio.sleep(1.1)
    
    # Troisième appel - devrait recalculer
    value = await cache_service.get_or_compute(
        "compute_key",
        compute_value,
        timedelta(seconds=1)
    )
    assert value == "computed_2"
    assert compute_count == 2

@pytest.mark.asyncio
async def test_cache_result_decorator():
    """Test du décorateur cache_result"""
    call_count = 0
    
    @cache_result(ttl_seconds=1)
    async def cached_function(param):
        nonlocal call_count
        call_count += 1
        return f"result_{param}_{call_count}"
    
    # Premier appel - devrait exécuter la fonction
    result = await cached_function("test")
    assert result == "result_test_1"
    assert call_count == 1
    
    # Deuxième appel avec mêmes paramètres - devrait utiliser le cache
    result = await cached_function("test")
    assert result == "result_test_1"
    assert call_count == 1
    
    # Appel avec paramètres différents - devrait exécuter la fonction
    result = await cached_function("other")
    assert result == "result_other_2"
    assert call_count == 2
    
    # Attendre l'expiration
    await asyncio.sleep(1.1)
    
    # Appel après expiration - devrait exécuter la fonction
    result = await cached_function("test")
    assert result == "result_test_3"
    assert call_count == 3

@pytest.mark.asyncio
async def test_cache_complex_objects(cache_service):
    """Test du cache avec des objets complexes"""
    complex_obj = {
        "string": "test",
        "number": 123,
        "list": [1, 2, 3],
        "dict": {"key": "value"},
        "none": None
    }
    
    # Test stockage et récupération
    await cache_service.set("complex_key", complex_obj)
    value = await cache_service.get("complex_key")
    assert value == complex_obj
    
    # Test avec le décorateur
    @cache_result(ttl_seconds=1)
    async def return_complex():
        return complex_obj
    
    result = await return_complex()
    assert result == complex_obj

@pytest.mark.asyncio
async def test_singleton_cache_service():
    """Test du singleton du service de cache"""
    service1 = get_cache_service()
    service2 = get_cache_service()
    
    assert service1 is service2
    
    # Test que les deux instances partagent le même cache
    await service1.set("singleton_key", "singleton_value")
    value = await service2.get("singleton_key")
    assert value == "singleton_value"