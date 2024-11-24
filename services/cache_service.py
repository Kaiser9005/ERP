"""
Service de cache pour l'optimisation des performances
"""

from typing import Any, Optional
from datetime import datetime, timedelta
import asyncio
from functools import lru_cache

class CacheService:
    """Service de gestion du cache"""
    
    def __init__(self):
        self._cache = {}
        self._expiration = {}
        
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if key not in self._cache:
            return None
            
        # Vérification expiration
        if key in self._expiration and datetime.now() > self._expiration[key]:
            del self._cache[key]
            del self._expiration[key]
            return None
            
        return self._cache[key]
        
    async def set(
        self,
        key: str,
        value: Any,
        expire_in: Optional[timedelta] = None
    ) -> None:
        """Stocke une valeur dans le cache"""
        self._cache[key] = value
        if expire_in:
            self._expiration[key] = datetime.now() + expire_in
            
    async def invalidate(self, key: str) -> None:
        """Invalide une entrée du cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expiration:
            del self._expiration[key]
            
    async def clear(self) -> None:
        """Vide le cache"""
        self._cache.clear()
        self._expiration.clear()
        
    @lru_cache(maxsize=128)
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
