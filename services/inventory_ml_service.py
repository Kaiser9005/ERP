"""
Service principal ML optimisé pour l'inventaire
Intègre tous les modules ML avec optimisations performance
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import torch
import numpy as np
from dataclasses import dataclass
from sqlalchemy.orm import Session

from models.inventory import Stock, MouvementStock
from services.cache_service import cache_result
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.ml.inventaire.base import ModeleInventaireML
from services.ml.inventaire.optimization import OptimiseurStock
from services.ml.inventaire.analysis import AnalyseurStock
from services.ml.inventaire.quality import PredicteurQualite
from services.ml.core.config import (
    get_model_config,
    get_cache_config,
    get_monitoring_config,
    get_resource_limits,
    ResourceLimits
)

logger = logging.getLogger(__name__)

@dataclass
class MLContext:
    """Contexte d'exécution ML"""
    device: str
    precision: str
    batch_size: int
    use_cache: bool
    profiling: bool
    resource_limits: ResourceLimits

class InventoryMLService:
    """Service principal ML optimisé pour l'inventaire"""

    def __init__(self, db: Session):
        # Configuration optimisée
        self.db = db
        self.resource_limits = get_resource_limits()
        self.monitoring_config = get_monitoring_config()
        self.cache_config = get_cache_config()
        
        # Initialisation modèles avec optimisations
        self.base_model = self._init_model(ModeleInventaireML())
        self.optimizer = self._init_model(OptimiseurStock())
        self.analyzer = self._init_model(AnalyseurStock())
        self.quality_predictor = self._init_model(PredicteurQualite())
        
        # Services externes
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        
        # État et optimisations
        self._is_trained = False
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if self.device == 'cuda':
            self._setup_gpu_optimizations()

    def _init_model(self, model: Any) -> Any:
        """
        Initialise modèle avec optimisations
        
        Args:
            model: Modèle à initialiser
            
        Returns:
            Modèle optimisé
        """
        config = get_model_config(model.__class__.__name__.lower())
        
        # Optimisations GPU
        if self.device == 'cuda':
            model = model.to(self.device)
            if config['compute']['torch_compile']:
                model = torch.compile(model)
            
        # Quantization si activée
        if config['inference']['quantization']['enabled']:
            model = torch.quantization.quantize_dynamic(
                model,
                {torch.nn.Linear},
                dtype=torch.qint8
            )
            
        return model

    def _setup_gpu_optimizations(self):
        """Configure optimisations GPU"""
        torch.cuda.empty_cache()
        torch.backends.cudnn.benchmark = True
        
        # Mixed precision
        if get_model_config('base')['training']['mixed_precision']:
            self.scaler = torch.cuda.amp.GradScaler()

    def _get_context(self, batch_size: Optional[int] = None) -> MLContext:
        """
        Prépare contexte ML optimisé
        
        Args:
            batch_size: Taille batch optionnelle
            
        Returns:
            Contexte ML
        """
        config = get_model_config('base')
        return MLContext(
            device=self.device,
            precision='mixed' if config['training']['mixed_precision'] else 'full',
            batch_size=batch_size or config['training']['batch_size'],
            use_cache=config['cache']['persistent_cache'],
            profiling=config['monitoring']['profiling']['enabled'],
            resource_limits=self.resource_limits
        )

    @cache_result(ttl_seconds=3600)
    def get_stock_insights(self,
                          stock: Stock,
                          mouvements: List[MouvementStock],
                          context: Optional[MLContext] = None) -> Dict:
        """
        Obtient analyses ML optimisées pour un stock
        
        Args:
            stock: Stock à analyser
            mouvements: Historique mouvements
            context: Contexte ML optionnel
            
        Returns:
            Dict analyses ML
        """
        if not self._is_trained:
            raise ValueError("Le service ML doit être entraîné avant utilisation")

        try:
            context = context or self._get_context()
            
            # Données externes
            weather_data = self.weather_service.get_current_conditions()
            iot_data = self.iot_service.get_sensor_data(stock.capteurs_id) if stock.capteurs_id else None

            # Prédictions optimisées
            with torch.cuda.amp.autocast(enabled=context.precision == 'mixed'):
                # Prédiction niveau optimal
                optimal_prediction = self._predict_with_profiling(
                    self.base_model.predict_stock_optimal,
                    stock, mouvements,
                    context=context
                )

                # Optimisation niveaux
                optimization = self._predict_with_profiling(
                    self.optimizer.optimize_stock_levels,
                    stock, mouvements, weather_data,
                    context=context
                )

                # Analyse patterns
                patterns = self._predict_with_profiling(
                    self.analyzer.analyze_stock_patterns,
                    stock, mouvements,
                    context=context
                )

                # Prédiction qualité
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
                    
                    quality_risk = self._predict_with_profiling(
                        self.quality_predictor.predict_quality_risk,
                        stock,
                        conditions_actuelles,
                        historique_conditions,
                        context=context
                    )

            result = {
                "niveau_optimal": optimal_prediction,
                "optimisation": optimization,
                "patterns": patterns,
                "risque_qualite": quality_risk,
                "date_analyse": datetime.now(datetime.timezone.utc).isoformat(),
                "meteo": weather_data,
                "donnees_iot": iot_data,
                "metadata": {
                    "device": context.device,
                    "precision": context.precision,
                    "batch_size": context.batch_size
                }
            }

            # Cache optimisé
            if context.use_cache:
                self._update_cache(stock.id, result)

            return result

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse ML du stock {stock.id}: {str(e)}")
            raise

    def _predict_with_profiling(self, 
                              func: callable,
                              *args,
                              context: MLContext,
                              **kwargs) -> Any:
        """
        Exécute prédiction avec profiling
        
        Args:
            func: Fonction à profiler
            *args: Arguments positionnels
            context: Contexte ML
            **kwargs: Arguments nommés
            
        Returns:
            Résultat fonction
        """
        if context.profiling and self.device == 'cuda':
            with torch.autograd.profiler.profile(use_cuda=True) as prof:
                result = func(*args, **kwargs)
                logger.debug(f"Profile {func.__name__}: {prof.key_averages().table()}")
        else:
            result = func(*args, **kwargs)
            
        return result

    def train(self, 
              stocks: List[Stock],
              mouvements: Dict[str, List[MouvementStock]],
              conditions_historiques: Optional[Dict[str, List[Dict]]] = None,
              quality_labels: Optional[Dict[str, int]] = None,
              context: Optional[MLContext] = None):
        """
        Entraîne modèles ML avec optimisations
        
        Args:
            stocks: Liste stocks
            mouvements: Historique mouvements
            conditions_historiques: Historique conditions optionnel
            quality_labels: Labels qualité optionnels
            context: Contexte ML optionnel
        """
        try:
            context = context or self._get_context()
            
            # Entraînement optimisé
            with torch.cuda.amp.autocast(enabled=context.precision == 'mixed'):
                # Base
                self._train_with_profiling(
                    self.base_model.train,
                    stocks, mouvements,
                    context=context
                )
                logger.info("Modèle de base entraîné")

                # Optimiseur
                self._train_with_profiling(
                    self.optimizer.train,
                    stocks, mouvements,
                    context=context
                )
                logger.info("Optimiseur entraîné")

                # Analyseur
                self._train_with_profiling(
                    self.analyzer.train,
                    stocks, mouvements,
                    context=context
                )
                logger.info("Analyseur entraîné")

                # Qualité
                if conditions_historiques and quality_labels:
                    self._train_with_profiling(
                        self.quality_predictor.train,
                        stocks,
                        conditions_historiques,
                        quality_labels,
                        context=context
                    )
                    logger.info("Prédicteur qualité entraîné")

            self._is_trained = True
            logger.info("Tous les modèles ML entraînés avec succès")

        except Exception as e:
            logger.error(f"Erreur entraînement modèles ML: {str(e)}")
            raise

    def _train_with_profiling(self,
                            func: callable,
                            *args,
                            context: MLContext,
                            **kwargs) -> None:
        """
        Entraîne avec profiling
        
        Args:
            func: Fonction entraînement
            *args: Arguments positionnels
            context: Contexte ML
            **kwargs: Arguments nommés
        """
        if context.profiling and self.device == 'cuda':
            with torch.autograd.profiler.profile(use_cuda=True) as prof:
                func(*args, **kwargs)
                logger.debug(f"Profile entraînement {func.__name__}: {prof.key_averages().table()}")
        else:
            func(*args, **kwargs)

    def save_models(self, base_path: str):
        """
        Sauvegarde modèles ML optimisés
        
        Args:
            base_path: Chemin base sauvegarde
        """
        try:
            # Sauvegarde avec métadonnées
            for name, model in [
                ('base', self.base_model),
                ('optimizer', self.optimizer),
                ('analyzer', self.analyzer),
                ('quality', self.quality_predictor)
            ]:
                path = f"{base_path}/{name}_model.pt"
                config = get_model_config(name)
                
                torch.save({
                    'model_state': model.state_dict(),
                    'config': config,
                    'metadata': {
                        'device': self.device,
                        'timestamp': datetime.now().isoformat()
                    }
                }, path)
                logger.info(f"Modèle {name} sauvegardé: {path}")

        except Exception as e:
            logger.error(f"Erreur sauvegarde modèles ML: {str(e)}")
            raise

    def load_models(self, base_path: str):
        """
        Charge modèles ML optimisés
        
        Args:
            base_path: Chemin base modèles
        """
        try:
            # Chargement avec vérification métadonnées
            for name, model in [
                ('base', self.base_model),
                ('optimizer', self.optimizer),
                ('analyzer', self.analyzer),
                ('quality', self.quality_predictor)
            ]:
                path = f"{base_path}/{name}_model.pt"
                checkpoint = torch.load(path, map_location=self.device)
                
                model.load_state_dict(checkpoint['model_state'])
                logger.info(f"Modèle {name} chargé: {path}")
                
                # Ré-optimisation si nécessaire
                if self.device == 'cuda':
                    model = self._init_model(model)

            self._is_trained = True
            logger.info("Tous les modèles ML chargés et optimisés")

        except Exception as e:
            logger.error(f"Erreur chargement modèles ML: {str(e)}")
            raise

    def _update_cache(self, key: str, data: Dict[str, Any]) -> None:
        """
        Met à jour cache optimisé
        
        Args:
            key: Clé cache
            data: Données à cacher
        """
        if self.cache_config['persistent']:
            # Implémentation Redis avec compression
            pass

    @property
    def is_trained(self) -> bool:
        """Vérifie si modèles sont entraînés"""
        return (self._is_trained and
                self.base_model.is_trained and
                self.optimizer.is_trained and
                self.analyzer.is_trained and
                self.quality_predictor.is_trained)
