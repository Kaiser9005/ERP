"""
Package de tests pour les fonctionnalités ML du tableau de bord.

Ce package contient :
- Tests unitaires
- Tests d'intégration
- Tests de performance
- Tests end-to-end
- Fixtures et utilitaires de test
"""

from pathlib import Path

# Chemins des répertoires de test ML
ML_TEST_DIR = Path(__file__).parent
ML_CACHE_DIR = ML_TEST_DIR / "cache"
ML_DATA_DIR = ML_TEST_DIR / "data"
ML_MODELS_DIR = ML_TEST_DIR / "models"

# Constantes pour les tests
DEFAULT_TEST_TIMEOUT = 60  # secondes
CACHE_EXPIRATION = 900  # 15 minutes
MAX_MEMORY_USAGE = 50 * 1024 * 1024  # 50MB
