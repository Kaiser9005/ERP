"""
Types de données pour les modèles d'apprentissage automatique de l'ERP FOFAL.
"""

from dataclasses import dataclass
from typing import Dict, List, Union, Optional
from datetime import datetime

@dataclass
class CaracteristiquesML:
    """Caractéristiques d'entrée pour les modèles ML."""
    donnees: Dict[str, Union[float, int, str]]
    date: datetime
    metadonnees: Optional[Dict[str, any]] = None

@dataclass
class PredictionML:
    """Résultat d'une prédiction ML."""
    valeur: Union[float, int, str]
    probabilite: float
    date_prediction: datetime
    metadonnees: Optional[Dict[str, any]] = None

@dataclass
class MetriquesML:
    """Métriques d'évaluation pour les modèles ML."""
    precision: float
    rappel: float
    f1_score: float
    date_evaluation: datetime
    details: Optional[Dict[str, float]] = None

@dataclass
class ParametresML:
    """Paramètres de configuration pour les modèles ML."""
    hyperparametres: Dict[str, Union[float, int, str]]
    configuration: Dict[str, any]
    date_modification: datetime

@dataclass
class ResultatOptimisation:
    """Résultat d'une optimisation d'hyperparamètres."""
    meilleurs_parametres: Dict[str, Union[float, int, str]]
    score: float
    historique_iterations: List[Dict[str, any]]
    date_optimisation: datetime
    metadonnees: Optional[Dict[str, any]] = None

@dataclass
class ResultatAnalyse:
    """Résultat d'une analyse ML."""
    metriques: Dict[str, float]
    graphiques: List[Dict[str, any]]
    recommandations: List[str]
    date_analyse: datetime
    details: Optional[Dict[str, any]] = None
