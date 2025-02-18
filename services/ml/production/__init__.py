"""
Module ML pour l'optimisation de la production agricole.

Ce module fournit des services d'apprentissage automatique pour :
- La prédiction des rendements
- L'optimisation des cycles de culture
- L'analyse de l'impact météo
- La prédiction de la qualité des récoltes
"""

from .base import BaseProductionML
from .rendement import PredicteurRendement
from .cycle import OptimiseurCycle
from .meteo import MeteoAnalyzer
from .qualite import QualitePredictor
from .service import ProductionMLService

__all__ = [
    'BaseProductionML',
    'ProductionMLService',
    'PredicteurRendement',
    'OptimiseurCycle',
    'MeteoAnalyzer',
    'QualitePredictor'
]
