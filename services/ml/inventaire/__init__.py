"""
Module ML pour l'inventaire
Fournit des services de prédiction et d'optimisation pour la gestion des stocks
"""

from .base import ModeleInventaireML
from .optimization import OptimiseurStock
from .analysis import AnalyseurStock
from .quality import PredicteurQualite

__all__ = [
    'ModeleInventaireML',
    'OptimiseurStock',
    'AnalyseurStock',
    'PredicteurQualite'
]
