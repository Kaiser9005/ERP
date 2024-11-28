"""
Classes de base pour les modèles d'apprentissage automatique de l'ERP FOFAL.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ModeleML(ABC):
    """Classe de base pour tous les modèles ML."""
    
    @abstractmethod
    def entrainer(self, donnees: Dict[str, Any]) -> None:
        """Entraîne le modèle avec les données fournies."""
        pass

    @abstractmethod
    def predire(self, donnees: Dict[str, Any]) -> Dict[str, Any]:
        """Effectue des prédictions sur les données fournies."""
        pass

    @abstractmethod
    def evaluer(self, donnees: Dict[str, Any]) -> Dict[str, float]:
        """Évalue les performances du modèle."""
        pass

    @abstractmethod
    def sauvegarder(self, chemin: str) -> None:
        """Sauvegarde le modèle sur le disque."""
        pass

    @abstractmethod
    def charger(self, chemin: str) -> None:
        """Charge le modèle depuis le disque."""
        pass

class OptimiseurML(ABC):
    """Interface pour l'optimisation des modèles ML."""
    
    @abstractmethod
    def optimiser(self, modele: ModeleML, donnees: Dict[str, Any]) -> Dict[str, Any]:
        """Optimise les hyperparamètres du modèle."""
        pass

    @abstractmethod
    def evaluer_optimisation(self, resultats: Dict[str, Any]) -> Dict[str, float]:
        """Évalue les résultats de l'optimisation."""
        pass

class AnalyseurML(ABC):
    """Interface pour l'analyse des données et résultats ML."""
    
    @abstractmethod
    def analyser_donnees(self, donnees: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les données d'entrée."""
        pass

    @abstractmethod
    def analyser_resultats(self, resultats: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse les résultats du modèle."""
        pass

    @abstractmethod
    def generer_rapport(self, analyses: Dict[str, Any]) -> str:
        """Génère un rapport d'analyse."""
        pass

class PredicteurML(ABC):
    """Interface pour les prédictions ML."""
    
    @abstractmethod
    def preparer_donnees(self, donnees: Dict[str, Any]) -> Dict[str, Any]:
        """Prépare les données pour la prédiction."""
        pass

    @abstractmethod
    def predire_batch(self, donnees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Effectue des prédictions sur un lot de données."""
        pass

    @abstractmethod
    def evaluer_predictions(self, predictions: List[Dict[str, Any]], 
                          reels: List[Dict[str, Any]]) -> Dict[str, float]:
        """Évalue la qualité des prédictions."""
        pass
