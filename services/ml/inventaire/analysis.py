"""
Module d'analyse des stocks utilisant le ML
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from models.inventory import Stock, MouvementStock, CategoryProduit
from services.cache_service import cache_result

class StockAnalyzer:
    """Analyseur de stocks utilisant le ML"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.cluster_model = KMeans(n_clusters=3, random_state=42)
        self._is_trained = False

    @cache_result(timeout=3600)
    def analyze_stock_patterns(self, 
                             stock: Stock,
                             mouvements: List[MouvementStock],
                             periode_jours: int = 90) -> Dict:
        """Analyse les patterns de stock sur une période donnée"""
        if not mouvements:
            return {
                "tendance": "stable",
                "saisonnalite": None,
                "anomalies": [],
                "recommendations": ["Données insuffisantes pour l'analyse"],
                "date_analyse": datetime.utcnow().isoformat()
            }

        # Création du DataFrame pour l'analyse
        df = self._prepare_dataframe(stock, mouvements, periode_jours)
        
        # Analyse des tendances
        tendance = self._analyze_trend(df)
        
        # Analyse de la saisonnalité
        saisonnalite = self._analyze_seasonality(df)
        
        # Détection des anomalies
        anomalies = self._detect_anomalies(df)
        
        # Génération des recommandations
        recommendations = self._generate_recommendations(
            stock, tendance, saisonnalite, anomalies
        )

        return {
            "tendance": tendance["direction"],
            "force_tendance": float(tendance["force"]),
            "saisonnalite": saisonnalite,
            "anomalies": anomalies,
            "recommendations": recommendations,
            "date_analyse": datetime.utcnow().isoformat()
        }

    def _prepare_dataframe(self, 
                          stock: Stock,
                          mouvements: List[MouvementStock],
                          periode_jours: int) -> pd.DataFrame:
        """Prépare les données pour l'analyse"""
        date_debut = datetime.utcnow() - timedelta(days=periode_jours)
        
        # Création du DataFrame des mouvements
        df = pd.DataFrame([{
            'date': m.date_mouvement,
            'quantite': m.quantite if m.type_mouvement == 'ENTREE' else -m.quantite,
            'type': m.type_mouvement,
            'cout': m.cout_unitaire or 0
        } for m in mouvements if m.date_mouvement >= date_debut])
        
        if df.empty:
            return pd.DataFrame()
        
        # Agrégation par jour
        df.set_index('date', inplace=True)
        df = df.resample('D').agg({
            'quantite': 'sum',
            'cout': 'mean'
        }).fillna(0)
        
        # Calcul du stock cumulé
        df['stock_cumule'] = df['quantite'].cumsum() + stock.quantite
        
        return df

    def _analyze_trend(self, df: pd.DataFrame) -> Dict:
        """Analyse la tendance des stocks"""
        if df.empty:
            return {"direction": "stable", "force": 0.0}

        # Calcul de la tendance linéaire
        x = np.arange(len(df))
        y = df['stock_cumule'].values
        z = np.polyfit(x, y, 1)
        pente = z[0]

        # Détermination de la force et direction
        force = abs(pente) / df['stock_cumule'].mean() if df['stock_cumule'].mean() != 0 else 0
        
        if force < 0.01:
            direction = "stable"
        elif pente > 0:
            direction = "hausse"
        else:
            direction = "baisse"

        return {
            "direction": direction,
            "force": float(force)
        }

    def _analyze_seasonality(self, df: pd.DataFrame) -> Optional[Dict]:
        """Analyse la saisonnalité des stocks"""
        if df.empty or len(df) < 30:  # Minimum 30 jours pour l'analyse
            return None

        # Analyse par jour de la semaine
        df['jour_semaine'] = df.index.dayofweek
        patterns_semaine = df.groupby('jour_semaine')['quantite'].mean()
        
        # Analyse par mois
        df['mois'] = df.index.month
        patterns_mois = df.groupby('mois')['quantite'].mean()

        return {
            "patterns_semaine": {
                str(jour): float(valeur)
                for jour, valeur in patterns_semaine.items()
            },
            "patterns_mois": {
                str(mois): float(valeur)
                for mois, valeur in patterns_mois.items()
            }
        }

    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Détecte les anomalies dans les mouvements de stock"""
        if df.empty:
            return []

        anomalies = []
        
        # Calcul des limites pour la détection d'anomalies
        mean = df['quantite'].mean()
        std = df['quantite'].std()
        upper_limit = mean + 2 * std
        lower_limit = mean - 2 * std

        # Détection des mouvements anormaux
        for date, row in df.iterrows():
            if abs(row['quantite']) > upper_limit or abs(row['quantite']) < lower_limit:
                anomalies.append({
                    "date": date.isoformat(),
                    "valeur": float(row['quantite']),
                    "type": "mouvement_anormal",
                    "description": "Mouvement de stock inhabituel détecté"
                })

        return anomalies

    def _generate_recommendations(self,
                                stock: Stock,
                                tendance: Dict,
                                saisonnalite: Optional[Dict],
                                anomalies: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []

        # Recommandations basées sur la tendance
        if tendance["direction"] == "hausse" and tendance["force"] > 0.1:
            recommendations.append(
                "Tendance à la hausse significative - Vérifier les niveaux de stock maximum"
            )
        elif tendance["direction"] == "baisse" and tendance["force"] > 0.1:
            recommendations.append(
                "Tendance à la baisse significative - Surveiller le seuil minimal"
            )

        # Recommandations basées sur la saisonnalité
        if saisonnalite:
            patterns_mois = saisonnalite["patterns_mois"]
            mois_actuel = str(datetime.utcnow().month)
            if mois_actuel in patterns_mois:
                if patterns_mois[mois_actuel] > 0:
                    recommendations.append(
                        "Période de forte activité - Augmenter les stocks de sécurité"
                    )
                elif patterns_mois[mois_actuel] < 0:
                    recommendations.append(
                        "Période de faible activité - Optimiser les niveaux de stock"
                    )

        # Recommandations basées sur les anomalies
        if len(anomalies) > 3:
            recommendations.append(
                "Nombreuses anomalies détectées - Revoir la politique de gestion des stocks"
            )

        # Recommandations basées sur les conditions de stockage
        if stock.conditions_stockage:
            if not stock.conditions_actuelles:
                recommendations.append(
                    "Conditions de stockage non surveillées - Installer des capteurs"
                )
            else:
                conditions = stock.conditions_actuelles
                if abs(conditions.get('temperature', 20) - 
                      stock.conditions_stockage.get('temperature', 20)) > 5:
                    recommendations.append(
                        "Écart de température significatif - Vérifier le système de régulation"
                    )

        return recommendations

    def train(self, stocks: List[Stock], mouvements: Dict[str, List[MouvementStock]]):
        """Entraîne l'analyseur sur les données historiques"""
        features = []
        
        for stock in stocks:
            stock_mouvements = mouvements.get(stock.id, [])
            if not stock_mouvements:
                continue

            # Extraction des caractéristiques
            avg_qty = np.mean([m.quantite for m in stock_mouvements])
            std_qty = np.std([m.quantite for m in stock_mouvements])
            freq = len(stock_mouvements) / 30  # Fréquence par jour
            
            features.append([avg_qty, std_qty, freq])

        if features:
            features = np.array(features)
            features_scaled = self.scaler.fit_transform(features)
            self.cluster_model.fit(features_scaled)
            self._is_trained = True

    @property
    def is_trained(self) -> bool:
        """Retourne si l'analyseur est entraîné"""
        return self._is_trained
