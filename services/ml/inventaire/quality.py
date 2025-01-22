"""
Module de prédiction de qualité des stocks utilisant le ML
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd

from models.inventory import Stock, MouvementStock
from services.cache_service import cache_result

class PredicteurQualite:  # Renommé pour correspondre à la nomenclature française
    """Prédicteur de qualité des stocks utilisant le ML"""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self._is_trained = False

    @cache_result(ttl_seconds=1800)
    def predict_quality_risk(self,
                           stock: Stock,
                           conditions_actuelles: Dict,
                           historique_conditions: List[Dict]) -> Dict:
        """Prédit le risque qualité pour un stock"""
        if not self._is_trained:
            raise ValueError("Le modèle doit être entraîné avant utilisation")

        # Préparation des features
        features = self._prepare_features(stock, conditions_actuelles, historique_conditions)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Prédiction du risque
        risk_proba = self.model.predict_proba(features_scaled)[0]
        risk_level = self._calculate_risk_level(risk_proba)
        
        # Analyse des facteurs de risque
        risk_factors = self._analyze_risk_factors(
            stock, conditions_actuelles, historique_conditions
        )

        return {
            "niveau_risque": risk_level,
            "probabilite": float(max(risk_proba)),
            "facteurs_risque": risk_factors,
            "recommendations": self._generate_recommendations(risk_level, risk_factors),
            "date_prediction": datetime.now(datetime.timezone.utc).isoformat()
        }

    def _prepare_features(self,
                         stock: Stock,
                         conditions: Dict,
                         historique: List[Dict]) -> np.ndarray:
        """Prépare les features pour le modèle ML"""
        features = []

        # Features des conditions actuelles
        features.extend([
            float(conditions.get('temperature', 0)),
            float(conditions.get('humidite', 0)),
            1 if conditions.get('ventilation', False) else 0
        ])

        # Features de l'historique
        if historique:
            temp_mean = np.mean([h.get('temperature', 0) for h in historique])
            temp_std = np.std([h.get('temperature', 0) for h in historique])
            hum_mean = np.mean([h.get('humidite', 0) for h in historique])
            hum_std = np.std([h.get('humidite', 0) for h in historique])
            features.extend([temp_mean, temp_std, hum_mean, hum_std])
        else:
            features.extend([0, 0, 0, 0])

        # Features du stock
        if stock.date_peremption:
            days_until_expiry = (stock.date_peremption - datetime.now(datetime.timezone.utc)).days
            features.append(float(days_until_expiry))
        else:
            features.append(0)

        return np.array(features)

    def _calculate_risk_level(self, probabilities: np.ndarray) -> str:
        """Calcule le niveau de risque basé sur les probabilités"""
        max_prob = max(probabilities)
        
        if max_prob >= 0.7:
            return "élevé"
        elif max_prob >= 0.4:
            return "moyen"
        else:
            return "faible"

    def _analyze_risk_factors(self,
                            stock: Stock,
                            conditions: Dict,
                            historique: List[Dict]) -> List[Dict]:
        """Analyse les facteurs de risque"""
        risk_factors = []

        # Vérification des conditions requises
        if stock.conditions_stockage:
            required_temp = stock.conditions_stockage.get('temperature')
            required_hum = stock.conditions_stockage.get('humidite')
            current_temp = conditions.get('temperature')
            current_hum = conditions.get('humidite')

            if required_temp and current_temp:
                temp_diff = abs(current_temp - required_temp)
                if temp_diff > 5:
                    risk_factors.append({
                        "type": "temperature",
                        "severite": "élevée" if temp_diff > 10 else "moyenne",
                        "description": f"Écart de température de {temp_diff:.1f}°C"
                    })

            if required_hum and current_hum:
                hum_diff = abs(current_hum - required_hum)
                if hum_diff > 10:
                    risk_factors.append({
                        "type": "humidite",
                        "severite": "élevée" if hum_diff > 20 else "moyenne",
                        "description": f"Écart d'humidité de {hum_diff:.1f}%"
                    })

        # Vérification de la péremption
        if stock.date_peremption:
            days_until_expiry = (stock.date_peremption - datetime.now(datetime.timezone.utc)).days
            if days_until_expiry <= 0:
                risk_factors.append({
                    "type": "peremption",
                    "severite": "élevée",
                    "description": "Produit périmé"
                })
            elif days_until_expiry <= 30:
                risk_factors.append({
                    "type": "peremption",
                    "severite": "moyenne",
                    "description": f"Péremption dans {days_until_expiry} jours"
                })

        # Analyse des variations historiques
        if historique:
            temp_std = np.std([h.get('temperature', 0) for h in historique])
            hum_std = np.std([h.get('humidite', 0) for h in historique])

            if temp_std > 5:
                risk_factors.append({
                    "type": "variation_temperature",
                    "severite": "moyenne",
                    "description": "Variations importantes de température"
                })

            if hum_std > 10:
                risk_factors.append({
                    "type": "variation_humidite",
                    "severite": "moyenne",
                    "description": "Variations importantes d'humidité"
                })

        return risk_factors

    def _generate_recommendations(self,
                                risk_level: str,
                                risk_factors: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur les risques"""
        recommendations = []

        if risk_level == "élevé":
            recommendations.append(
                "Inspection immédiate du stock requise"
            )

        for factor in risk_factors:
            if factor["type"] == "temperature":
                recommendations.append(
                    "Ajuster le système de régulation thermique"
                )
            elif factor["type"] == "humidite":
                recommendations.append(
                    "Vérifier le système de contrôle d'humidité"
                )
            elif factor["type"] == "peremption":
                if factor["severite"] == "élevée":
                    recommendations.append(
                        "Retirer les produits périmés du stock"
                    )
                else:
                    recommendations.append(
                        "Planifier l'écoulement des produits proche péremption"
                    )
            elif factor["type"].startswith("variation_"):
                recommendations.append(
                    "Stabiliser les conditions de stockage"
                )

        if not recommendations:
            recommendations.append(
                "Maintenir la surveillance régulière"
            )

        return recommendations

    def train(self, 
              stocks: List[Stock],
              conditions_historiques: Dict[str, List[Dict]],
              quality_labels: Dict[str, int]):
        """Entraîne le prédicteur de qualité"""
        X, y = [], []
        
        for stock in stocks:
            historique = conditions_historiques.get(stock.id, [])
            if not historique:
                continue

            # Conditions actuelles (dernière entrée de l'historique)
            conditions_actuelles = historique[-1]
            
            # Préparation des features
            features = self._prepare_features(
                stock, conditions_actuelles, historique[:-1]
            )
            
            X.append(features)
            y.append(quality_labels.get(stock.id, 0))

        if X and y:
            X = np.array(X)
            y = np.array(y)
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self._is_trained = True

    @property
    def is_trained(self) -> bool:
        """Retourne si le prédicteur est entraîné"""
        return self._is_trained
