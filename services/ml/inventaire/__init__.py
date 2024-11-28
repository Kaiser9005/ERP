"""
Module ML pour l'inventaire
Fournit des services de prédiction et d'optimisation pour la gestion des stocks
"""

from .base import InventoryMLModel as ModeleInventaireML
from .optimization import StockOptimizer as OptimiseurStock
from .analysis import StockAnalyzer as AnalyseurStock
from .quality import QualityPredictor as PredicteurQualite

__all__ = [
    'ModeleInventaireML',
    'OptimiseurStock',
    'AnalyseurStock',
    'PredicteurQualite'
]
