"""
Tests pour le module ML d'inventaire
"""

from .test_base import *
from .test_optimization import *
from .test_analysis import *
from .test_quality import *
from .test_integration import *

__all__ = [
    'TestModeleInventaireML',
    'TestOptimiseurInventaire',
    'TestAnalyseurInventaire',
    'TestControleurQualite',
    'TestIntegrationInventaireML'
]
