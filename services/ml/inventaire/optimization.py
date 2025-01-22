"""
Module d'optimisation des stocks utilisant le ML
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

from models.inventory import Stock, MouvementStock, CategoryProduit
from services.cache_service import cache_result
from .base import ModeleInventaireML

class OptimiseurStock:  # Renommé pour correspondre à l'import attendu
    """Optimiseur de stocks utilisant le ML"""

    def __init__(self):
        self.base_model = ModeleInventaireML()
        self.optimizer = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self._is_trained = False

    @cache_result(ttl_seconds=3600)
    def optimize_stock_levels(self, 
                            stock: Stock, 
                            mouvements: List[MouvementStock],
                            weather_data: Optional[Dict] = None) -> Dict:
        """Optimise les niveaux de stock en tenant compte des conditions"""
        if not self._is_trained:
            raise ValueError("L'optimiseur doit être entraîné avant utilisation")

        # Prédiction du niveau optimal de base
        base_prediction = self.base_model.predict_stock_optimal(stock, mouvements)
        
        # Facteurs d'ajustement
        adjustments = self._calculate_adjustments(stock, mouvements, weather_data)
        
        # Niveau optimal ajusté
        optimal_level = base_prediction["niveau_optimal"] * adjustments["facteur_global"]

        return {
            "niveau_optimal": float(optimal_level),
            "niveau_min": float(optimal_level * 0.8),  # Marge de sécurité
            "niveau_max": float(optimal_level * 1.2),  # Capacité maximale
            "ajustements": adjustments,
            "confiance": float(base_prediction["confiance"]),
            "date_optimisation": datetime.now(datetime.timezone.utc).isoformat()
        }

    def _calculate_adjustments(self, 
                             stock: Stock, 
                             mouvements: List[MouvementStock],
                             weather_data: Optional[Dict]) -> Dict:
        """Calcule les facteurs d'ajustement pour l'optimisation"""
        adjustments = {
            "saisonnalite": self._seasonal_factor(stock, mouvements),
            "peremption": self._expiration_factor(stock),
            "meteo": self._weather_factor(stock, weather_data),
            "tendance": self._trend_factor(mouvements)
        }
        
        # Facteur global combinant tous les ajustements
        facteur_global = np.mean(list(adjustments.values()))
        adjustments["facteur_global"] = float(facteur_global)

        return adjustments

    def _seasonal_factor(self, stock: Stock, mouvements: List[MouvementStock]) -> float:
        """Calcule le facteur saisonnier"""
        if not mouvements:
            return 1.0

        # Analyse des mouvements par mois
        df = pd.DataFrame([{
            'date': m.date_mouvement,
            'quantite': m.quantite
        } for m in mouvements])
        
        if df.empty:
            return 1.0

        df['month'] = df['date'].dt.month
        monthly_avg = df.groupby('month')['quantite'].mean()
        
        # Facteur basé sur le mois actuel
        current_month = datetime.now(datetime.timezone.utc).month
        if current_month in monthly_avg.index:
            month_factor = monthly_avg[current_month] / monthly_avg.mean()
            return float(np.clip(month_factor, 0.8, 1.2))
        
        return 1.0

    def _expiration_factor(self, stock: Stock) -> float:
        """Calcule le facteur lié à la péremption"""
        if not stock.date_peremption:
            return 1.0

        days_until_expiry = (stock.date_peremption - datetime.now(datetime.timezone.utc)).days
        
        if days_until_expiry <= 0:
            return 0.5  # Réduction drastique pour produits périmés
        elif days_until_expiry <= 30:
            return 0.8  # Réduction pour produits proche péremption
        elif days_until_expiry <= 90:
            return 0.9  # Légère réduction pour anticiper
        
        return 1.0

    def _weather_factor(self, stock: Stock, weather_data: Optional[Dict]) -> float:
        """Calcule le facteur météorologique"""
        if not weather_data or not stock.conditions_stockage:
            return 1.0

        conditions_requises = stock.conditions_stockage
        
        # Vérification des conditions optimales
        temp_ok = abs(weather_data.get('temperature', 20) - 
                     conditions_requises.get('temperature', 20)) <= 5
        humidity_ok = abs(weather_data.get('humidite', 50) - 
                         conditions_requises.get('humidite', 50)) <= 10

        if temp_ok and humidity_ok:
            return 1.0
        elif temp_ok or humidity_ok:
            return 0.9
        else:
            return 0.8

    def _trend_factor(self, mouvements: List[MouvementStock]) -> float:
        """Calcule le facteur de tendance"""
        if not mouvements:
            return 1.0

        # Analyse des derniers mouvements
        recent_mouvements = [m for m in mouvements 
                           if m.date_mouvement >= datetime.now(datetime.timezone.utc) - timedelta(days=30)]
        
        if not recent_mouvements:
            return 1.0

        # Calcul de la tendance
        quantities = [m.quantite for m in recent_mouvements]
        trend = np.polyfit(range(len(quantities)), quantities, deg=1)[0]
        
        # Normalisation de la tendance
        if trend > 0:
            return float(np.clip(1 + (trend / max(quantities)), 1.0, 1.2))
        else:
            return float(np.clip(1 + (trend / max(quantities)), 0.8, 1.0))

    def train(self, stocks: List[Stock], mouvements: Dict[str, List[MouvementStock]]):
        """Entraîne l'optimiseur"""
        # Entraînement du modèle de base
        self.base_model.train(stocks, mouvements)
        
        # Préparation des données pour l'optimiseur
        X, y = [], []
        
        for stock in stocks:
            stock_mouvements = mouvements.get(stock.id, [])
            if not stock_mouvements:
                continue

            # Features pour l'optimisation
            features = [
                stock.quantite,
                len(stock_mouvements),
                np.mean([m.quantite for m in stock_mouvements]),
                np.std([m.quantite for m in stock_mouvements]),
                self._seasonal_factor(stock, stock_mouvements),
                self._expiration_factor(stock),
                self._trend_factor(stock_mouvements)
            ]
            
            X.append(features)
            y.append(stock.quantite)  # Objectif : niveau optimal réel

        if X and y:
            X = np.array(X)
            y = np.array(y)
            self.optimizer.fit(X, y)
            self._is_trained = True

    @property
    def is_trained(self) -> bool:
        """Retourne si l'optimiseur est entraîné"""
        return self._is_trained and self.base_model.is_trained
