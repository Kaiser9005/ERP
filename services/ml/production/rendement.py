"""
Module pour la prédiction des rendements de production.
"""

from typing import Dict, Any, List
from datetime import date
import numpy as np
from sqlalchemy.orm import Session

from .base import BaseProductionML
from services.weather_service import WeatherService
from services.iot_service import IoTService

class PredicteurRendement(BaseProductionML):
    """Service ML pour la prédiction des rendements"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)

    async def predict_rendement(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Prédit le rendement d'une parcelle pour une période donnée"""
        # Récupération des données historiques
        historique = await self._get_historique_rendements(parcelle_id)
        
        # Récupération des données météo
        meteo = await self.weather_service.get_historical_data(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Récupération des données IoT
        iot_data = await self.iot_service.get_sensor_data(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Calcul des features
        features = self._calculate_features(historique, meteo, iot_data)
        
        # Prédiction avec le modèle
        prediction = await self._predict_with_model(features)
        
        # Calcul de l'intervalle de confiance
        confidence = self._calculate_confidence(prediction, historique)
        
        return {
            "rendement_prevu": float(prediction),
            "intervalle_confiance": confidence,
            "facteurs_impact": await self._analyze_impact_factors(features)
        }

    async def _predict_with_model(
        self,
        features: np.ndarray
    ) -> float:
        """Prédit le rendement avec le modèle ML"""
        # TODO: Implémenter le modèle ML
        # Pour l'instant, utilise une moyenne pondérée
        weights = np.array([0.4, 0.1, 0.1, 0.2, 0.1, 0.1, 0.3, 0.1, 0.1])
        return float(np.sum(features * weights))

    def _calculate_confidence(
        self,
        prediction: float,
        historique: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calcule l'intervalle de confiance de la prédiction"""
        if not historique:
            return {"min": prediction * 0.8, "max": prediction * 1.2}
            
        std = np.std([h["quantite"] for h in historique])
        return {
            "min": prediction - 2 * std,
            "max": prediction + 2 * std
        }

    async def _analyze_impact_factors(
        self,
        features: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Analyse les facteurs d'impact sur la prédiction"""
        return [
            {
                "facteur": "Historique",
                "impact": 0.4,
                "description": "Basé sur les rendements précédents"
            },
            {
                "facteur": "Météo",
                "impact": 0.3,
                "description": "Conditions météorologiques prévues"
            },
            {
                "facteur": "IoT",
                "impact": 0.3,
                "description": "Données des capteurs"
            }
        ]
