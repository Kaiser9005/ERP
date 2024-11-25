"""
Service principal ML pour l'inventaire
Intègre tous les modules ML pour l'inventaire
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging

from models.inventory import Stock, MouvementStock
from services.cache_service import cache_result
from services.weather_service import WeatherService
from services.iot_service import IoTService
from .inventory_ml.base import InventoryMLModel
from .inventory_ml.optimization import StockOptimizer
from .inventory_ml.analysis import StockAnalyzer
from .inventory_ml.quality import QualityPredictor

logger = logging.getLogger(__name__)

class InventoryMLService:
    """Service principal ML pour l'inventaire"""

    def __init__(self):
        self.base_model = InventoryMLModel()
        self.optimizer = StockOptimizer()
        self.analyzer = StockAnalyzer()
        self.quality_predictor = QualityPredictor()
        self.weather_service = WeatherService()
        self.iot_service = IoTService()
        self._is_trained = False

    @cache_result(timeout=3600)
    def get_stock_insights(self,
                          stock: Stock,
                          mouvements: List[MouvementStock]) -> Dict:
        """Obtient toutes les analyses ML pour un stock"""
        if not self._is_trained:
            raise ValueError("Le service ML doit être entraîné avant utilisation")

        try:
            # Récupération des données météo et IoT
            weather_data = self.weather_service.get_current_conditions()
            iot_data = self.iot_service.get_sensor_data(stock.capteurs_id) if stock.capteurs_id else None

            # Prédiction du niveau optimal
            optimal_prediction = self.base_model.predict_stock_optimal(stock, mouvements)

            # Optimisation des niveaux
            optimization = self.optimizer.optimize_stock_levels(
                stock, mouvements, weather_data
            )

            # Analyse des patterns
            patterns = self.analyzer.analyze_stock_patterns(stock, mouvements)

            # Prédiction de la qualité
            quality_risk = None
            if iot_data:
                conditions_actuelles = {
                    'temperature': iot_data.get('temperature'),
                    'humidite': iot_data.get('humidite'),
                    'ventilation': iot_data.get('ventilation', False)
                }
                historique_conditions = self.iot_service.get_historical_data(
                    stock.capteurs_id,
                    days=30
                ) if stock.capteurs_id else []
                
                quality_risk = self.quality_predictor.predict_quality_risk(
                    stock,
                    conditions_actuelles,
                    historique_conditions
                )

            return {
                "niveau_optimal": optimal_prediction,
                "optimisation": optimization,
                "patterns": patterns,
                "risque_qualite": quality_risk,
                "date_analyse": datetime.now(datetime.timezone.utc).isoformat(),
                "meteo": weather_data,
                "donnees_iot": iot_data
            }

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse ML du stock {stock.id}: {str(e)}")
            raise

    def train(self, 
              stocks: List[Stock],
              mouvements: Dict[str, List[MouvementStock]],
              conditions_historiques: Optional[Dict[str, List[Dict]]] = None,
              quality_labels: Optional[Dict[str, int]] = None):
        """Entraîne tous les modèles ML"""
        try:
            # Entraînement du modèle de base
            self.base_model.train(stocks, mouvements)
            logger.info("Modèle de base entraîné avec succès")

            # Entraînement de l'optimiseur
            self.optimizer.train(stocks, mouvements)
            logger.info("Optimiseur entraîné avec succès")

            # Entraînement de l'analyseur
            self.analyzer.train(stocks, mouvements)
            logger.info("Analyseur entraîné avec succès")

            # Entraînement du prédicteur de qualité
            if conditions_historiques and quality_labels:
                self.quality_predictor.train(
                    stocks,
                    conditions_historiques,
                    quality_labels
                )
                logger.info("Prédicteur de qualité entraîné avec succès")

            self._is_trained = True
            logger.info("Tous les modèles ML ont été entraînés avec succès")

        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement des modèles ML: {str(e)}")
            raise

    def save_models(self, base_path: str):
        """Sauvegarde tous les modèles ML"""
        try:
            self.base_model.save_model(f"{base_path}/base_model.joblib")
            logger.info("Modèle de base sauvegardé")
            
            # Autres sauvegardes à implémenter selon les besoins
            
            logger.info("Tous les modèles ML ont été sauvegardés")

        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des modèles ML: {str(e)}")
            raise

    def load_models(self, base_path: str):
        """Charge tous les modèles ML"""
        try:
            self.base_model.load_model(f"{base_path}/base_model.joblib")
            logger.info("Modèle de base chargé")
            
            # Autres chargements à implémenter selon les besoins
            
            self._is_trained = True
            logger.info("Tous les modèles ML ont été chargés")

        except Exception as e:
            logger.error(f"Erreur lors du chargement des modèles ML: {str(e)}")
            raise

    @property
    def is_trained(self) -> bool:
        """Retourne si tous les modèles sont entraînés"""
        return (self._is_trained and
                self.base_model.is_trained and
                self.optimizer.is_trained and
                self.analyzer.is_trained and
                self.quality_predictor.is_trained)
