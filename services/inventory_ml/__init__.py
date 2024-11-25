"""
Module ML pour l'inventaire
Fournit des services de prédiction et d'optimisation pour la gestion des stocks
"""

from .base import InventoryMLModel
from .optimization import StockOptimizer
from .analysis import StockAnalyzer
from .quality import QualityPredictor

__all__ = [
    'InventoryMLModel',
    'StockOptimizer',
    'StockAnalyzer',
    'QualityPredictor'
]
