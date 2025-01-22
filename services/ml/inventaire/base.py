"""
Modèle ML de base pour l'inventaire
"""

from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

from models.inventory import CategoryProduit, Stock, MouvementStock
from services.cache_service import cache_result

class ModeleInventaireML:  # Renommé pour correspondre à l'import attendu
    """Modèle ML de base pour les prédictions d'inventaire"""

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self._is_trained = False

    def _prepare_features(self, stock: Stock, mouvements: List[MouvementStock]) -> np.ndarray:
        """Prépare les features pour le modèle ML"""
        features = []
        
        # Features du stock
        features.extend([
            stock.quantite,
            float(stock.valeur_unitaire or 0),
            1 if stock.date_peremption else 0,
            (stock.date_peremption - datetime.now(datetime.timezone.utc)).days if stock.date_peremption else 0
        ])

        # Features des conditions actuelles
        if stock.conditions_actuelles:
            conditions = stock.conditions_actuelles
            features.extend([
                float(conditions.get('temperature', 0)),
                float(conditions.get('humidite', 0)),
                1 if conditions.get('ventilation', False) else 0
            ])
        else:
            features.extend([0, 0, 0])

        # Features des mouvements
        if mouvements:
            avg_quantite = np.mean([m.quantite for m in mouvements])
            avg_cout = np.mean([m.cout_unitaire or 0 for m in mouvements])
            freq_mouvements = len(mouvements) / 30  # Mouvements par jour sur 30 jours
            features.extend([avg_quantite, avg_cout, freq_mouvements])
        else:
            features.extend([0, 0, 0])

        return np.array(features).reshape(1, -1)

    @cache_result(ttl_seconds=3600)  # Changé de timeout à ttl_seconds
    def predict_stock_optimal(self, stock: Stock, mouvements: List[MouvementStock]) -> Dict:
        """Prédit le niveau de stock optimal"""
        if not self._is_trained:
            raise ValueError("Le modèle doit être entraîné avant de faire des prédictions")

        features = self._prepare_features(stock, mouvements)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]

        return {
            "niveau_optimal": float(prediction),
            "confiance": float(self.model.score(features_scaled, [stock.quantite])),
            "date_prediction": datetime.now(datetime.timezone.utc).isoformat()
        }

    def train(self, stocks: List[Stock], mouvements: Dict[str, List[MouvementStock]]):
        """Entraîne le modèle ML"""
        X, y = [], []

        for stock in stocks:
            stock_mouvements = mouvements.get(stock.id, [])
            features = self._prepare_features(stock, stock_mouvements)
            X.append(features.flatten())
            y.append(stock.quantite)

        X = np.array(X)
        y = np.array(y)

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self._is_trained = True

    def save_model(self, path: str):
        """Sauvegarde le modèle ML"""
        if not self._is_trained:
            raise ValueError("Le modèle doit être entraîné avant d'être sauvegardé")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self._is_trained
        }
        joblib.dump(model_data, path)

    def load_model(self, path: str):
        """Charge le modèle ML"""
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self._is_trained = model_data['is_trained']

    @property
    def is_trained(self) -> bool:
        """Retourne si le modèle est entraîné"""
        return self._is_trained
