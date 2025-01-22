"""
Service de cache pour l'optimisation des performances
"""

from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import asyncio
from functools import wraps
import json
import redis
import pickle
from core.config import REDIS_CONFIG

class CacheService:
    """Service de gestion du cache Redis"""
    
    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS_CONFIG["HOST"],
            port=REDIS_CONFIG["PORT"],
            decode_responses=True
        )
        
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        try:
            value = self.redis.get(key)
            if value is None:
                return None
            return pickle.loads(value.encode())
        except Exception as e:
            print(f"Erreur lors de la récupération du cache : {str(e)}")
            return None
            
    async def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> None:
        """Stocke une valeur dans le cache"""
        try:
            pickled_value = pickle.dumps(value)
            if expire_in:
                self.redis.setex(key, expire_in.total_seconds(), pickled_value)
            else:
                self.redis.set(key, pickled_value)
        except Exception as e:
            print(f"Erreur lors du stockage dans le cache : {str(e)}")
            
    async def invalidate(self, key: str) -> None:
        """Invalide une entrée du cache"""
        try:
            self.redis.delete(key)
        except Exception as e:
            print(f"Erreur lors de l'invalidation du cache : {str(e)}")
            
    async def clear(self) -> None:
        """Vide le cache"""
        try:
            self.redis.flushdb()
        except Exception as e:
            print(f"Erreur lors du vidage du cache : {str(e)}")
        
    async def get_or_compute(
        self,
        key: str,
        compute_func: callable,
        expire_in: Optional[timedelta] = None
    ) -> Any:
        """Récupère du cache ou calcule si absent"""
        value = await self.get(key)
        if value is not None:
            return value
            
        value = await compute_func()
        await self.set(key, value, expire_in)
        return value

def cache_result(ttl_seconds: int = 3600):
    """Décorateur pour mettre en cache le résultat d'une fonction"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Création d'une clé unique basée sur la fonction et ses arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Initialisation du service de cache
            cache_service = CacheService()
            
            # Tentative de récupération depuis le cache
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
                
            # Calcul du résultat si non présent dans le cache
            result = await func(*args, **kwargs)
            
            # Stockage dans le cache
            await cache_service.set(
                cache_key,
                result,
                expire_in=timedelta(seconds=ttl_seconds)
            )
            
            return result
        return wrapper
    return decorator

# Instance singleton du service de cache
_cache_service = None

def get_cache_service() -> CacheService:
    """Retourne l'instance singleton du service de cache"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
