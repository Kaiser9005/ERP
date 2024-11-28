"""
Interfaces et configurations ML de base pour l'ERP FOFAL.
"""

from .base import ModeleML, OptimiseurML, AnalyseurML, PredicteurML
from .config import ConfigurationML
from .types import (
    CaracteristiquesML,
    PredictionML,
    MetriquesML,
    ParametresML,
    ResultatOptimisation,
    ResultatAnalyse
)

__all__ = [
    'ModeleML',
    'OptimiseurML', 
    'AnalyseurML',
    'PredicteurML',
    'ConfigurationML',
    'CaracteristiquesML',
    'PredictionML',
    'MetriquesML',
    'ParametresML',
    'ResultatOptimisation',
    'ResultatAnalyse'
]
