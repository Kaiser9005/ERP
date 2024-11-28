"""
Module d'analyse financière et comptable intégrée avec ML
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
import numpy as np
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from models.comptabilite import (
    CompteComptable, 
    EcritureComptable,
    TypeCompte
)
from models.finance import Transaction, Budget
from models.production import Parcelle
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService

class AnalyseFinanceCompta:
    """Analyse intégrée finance-comptabilité avec ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db)
        self.cache = CacheService()

    async def get_analyse_parcelle(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        include_predictions: bool = True
    ) -> Dict[str, Any]:
        """Analyse financière détaillée d'une parcelle avec ML"""
        # Récupération des données de base
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)

        # Analyse intégrée
        transactions = await self._get_transactions_parcelle(
            parcelle_id, 
            date_debut,
            date_fin
        )
        
        ecritures = await self._get_ecritures_parcelle(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Données IoT et météo
        iot_data = await self.iot_service.get_parcelle_data(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        weather_data = await self.weather_service.get_historical_data(
            date_debut,
            date_fin
        )
        
        # Calcul des indicateurs
        indicateurs = await self._calculer_indicateurs(
            transactions,
            ecritures,
            parcelle.surface
        )
        
        # Analyse ML si demandée
        ml_analysis = None
        if include_predictions:
            ml_analysis = await self._analyze_with_ml(
                parcelle_id,
                transactions,
                ecritures,
                iot_data,
                weather_data
            )
        
        return {
            "parcelle": {
                "id": parcelle.id,
                "code": parcelle.code,
                "surface": parcelle.surface,
                "culture": parcelle.culture_actuelle
            },
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            },
            "indicateurs": indicateurs,
            "transactions": {
                "count": len(transactions),
                "total_recettes": sum(t.montant for t in transactions if t.type_transaction == "RECETTE"),
                "total_depenses": sum(t.montant for t in transactions if t.type_transaction == "DEPENSE")
            },
            "comptabilite": {
                "count": len(ecritures),
                "total_debit": sum(e.debit or 0 for e in ecritures),
                "total_credit": sum(e.credit or 0 for e in ecritures)
            },
            "ml_analysis": ml_analysis
        }

    async def predict_performance(
        self,
        parcelle_id: str,
        months_ahead: int = 3
    ) -> Dict[str, Any]:
        """Prédit la performance financière future"""
        # Données historiques
        historical = await self._get_historical_data(parcelle_id)
        
        # Prévisions météo
        weather = await self.weather_service.get_long_term_forecast(months_ahead)
        
        # Données IoT
        iot = await self.iot_service.get_parcelle_data(
            parcelle_id,
            date.today(),
            date.today() + timedelta(days=30*months_ahead)
        )
        
        # Calcul features
        features = self._calculate_prediction_features(
            historical,
            weather,
            iot
        )
        
        # Prédiction
        predictions = []
        for i in range(months_ahead):
            month_date = date.today() + timedelta(days=30*i)
            prediction = await self._predict_month_performance(
                parcelle_id,
                month_date,
                features
            )
            predictions.append({
                "month": month_date.strftime("%Y-%m"),
                "revenue": prediction["revenue"],
                "costs": prediction["costs"],
                "margin": prediction["revenue"] - prediction["costs"],
                "confidence": prediction["confidence"],
                "weather_impact": prediction["weather_impact"]
            })
            
        return {
            "predictions": predictions,
            "risk_factors": await self._analyze_risk_factors(predictions),
            "recommendations": await self._generate_ml_recommendations(
                parcelle_id,
                predictions
            )
        }

    async def optimize_costs(
        self,
        parcelle_id: str,
        target_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Optimise les coûts avec ML"""
        # Données actuelles
        current_costs = await self._get_current_costs(parcelle_id)
        
        # Impact météo
        weather_impact = await self.weather_service.get_forecast_impact(
            target_date or date.today()
        )
        
        # Données IoT
        iot_data = await self.iot_service.get_latest_data(parcelle_id)
        
        # Optimisation
        optimization = await self._optimize_with_ml(
            current_costs,
            weather_impact,
            iot_data
        )
        
        return {
            "current_costs": current_costs,
            "optimized_costs": optimization["costs"],
            "potential_savings": optimization["savings"],
            "implementation_plan": optimization["plan"],
            "risk_assessment": optimization["risks"]
        }

    async def _analyze_with_ml(
        self,
        parcelle_id: str,
        transactions: List[Transaction],
        ecritures: List[EcritureComptable],
        iot_data: Dict[str, Any],
        weather_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse avancée avec ML"""
        # Préparation features
        features = self._prepare_ml_features(
            transactions,
            ecritures,
            iot_data,
            weather_data
        )
        
        # Prédictions
        predictions = await self._run_ml_predictions(features)
        
        # Analyse risques
        risks = await self._analyze_ml_risks(
            parcelle_id,
            predictions,
            weather_data
        )
        
        # Recommandations
        recommendations = await self._generate_ml_recommendations(
            parcelle_id,
            predictions
        )
        
        return {
            "predictions": predictions,
            "risks": risks,
            "recommendations": recommendations,
            "confidence_scores": {
                "predictions": 0.85,
                "risks": 0.80,
                "recommendations": 0.75
            }
        }

    def _prepare_ml_features(
        self,
        transactions: List[Transaction],
        ecritures: List[EcritureComptable],
        iot_data: Dict[str, Any],
        weather_data: Dict[str, Any]
    ) -> np.ndarray:
        """Prépare les features pour le ML"""
        features = []
        
        # Features transactions
        if transactions:
            features.extend([
                len(transactions),
                np.mean([t.montant for t in transactions if t.type_transaction == "RECETTE"]),
                np.mean([t.montant for t in transactions if t.type_transaction == "DEPENSE"])
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features comptables
        if ecritures:
            features.extend([
                len(ecritures),
                np.mean([e.debit or 0 for e in ecritures]),
                np.mean([e.credit or 0 for e in ecritures])
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features IoT
        features.extend([
            iot_data.get("temperature_avg", 0),
            iot_data.get("humidity_avg", 0),
            iot_data.get("soil_moisture_avg", 0)
        ])
        
        # Features météo
        features.extend([
            weather_data.get("temperature_avg", 0),
            weather_data.get("precipitation_avg", 0),
            weather_data.get("wind_speed_avg", 0)
        ])
        
        return np.array(features)

    async def _run_ml_predictions(
        self,
        features: np.ndarray
    ) -> Dict[str, Any]:
        """Exécute les prédictions ML"""
        # TODO: Implémenter modèle ML
        # Pour l'instant, utilise une moyenne pondérée
        weights = np.array([0.1] * len(features))
        prediction = float(np.sum(features * weights))
        
        return {
            "revenue": prediction * 1.1,
            "costs": prediction * 0.8,
            "margin": prediction * 0.3,
            "growth_potential": 0.15,
            "risk_score": 0.25
        }

    async def _analyze_ml_risks(
        self,
        parcelle_id: str,
        predictions: Dict[str, Any],
        weather_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyse des risques avec ML"""
        risks = []
        
        # Risques financiers
        if predictions["margin"] < predictions["costs"] * 0.2:
            risks.append({
                "type": "FINANCIAL",
                "severity": "HIGH",
                "description": "Marge faible",
                "probability": 0.8,
                "impact": "Rentabilité menacée",
                "mitigation": [
                    "Optimiser coûts",
                    "Revoir tarification"
                ]
            })
            
        # Risques météo
        if weather_data.get("precipitation_avg", 0) > 100:
            risks.append({
                "type": "WEATHER",
                "severity": "MEDIUM",
                "description": "Fortes précipitations",
                "probability": 0.6,
                "impact": "Augmentation coûts maintenance",
                "mitigation": [
                    "Renforcer drainage",
                    "Adapter planning"
                ]
            })
            
        return risks

    async def _generate_ml_recommendations(
        self,
        parcelle_id: str,
        predictions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur ML"""
        recommendations = []
        
        # Recommandations coûts
        if predictions.get("costs", 0) > predictions.get("revenue", 0) * 0.8:
            recommendations.append({
                "type": "COST",
                "priority": "HIGH",
                "description": "Coûts élevés détectés",
                "actions": [
                    "Analyser postes principaux",
                    "Identifier optimisations possibles",
                    "Revoir fournisseurs"
                ],
                "expected_impact": {
                    "savings": "10-15%",
                    "timeline": "3-6 mois"
                }
            })
            
        # Recommandations croissance
        if predictions.get("growth_potential", 0) > 0.1:
            recommendations.append({
                "type": "GROWTH",
                "priority": "MEDIUM",
                "description": "Potentiel croissance identifié",
                "actions": [
                    "Augmenter production",
                    "Optimiser rendement",
                    "Explorer nouveaux marchés"
                ],
                "expected_impact": {
                    "revenue_increase": "15-20%",
                    "timeline": "6-12 mois"
                }
            })
            
        return recommendations

    async def _get_historical_data(
        self,
        parcelle_id: str,
        months_back: int = 12
    ) -> Dict[str, Any]:
        """Récupère les données historiques"""
        start_date = date.today() - timedelta(days=30*months_back)
        
        transactions = await self._get_transactions_parcelle(
            parcelle_id,
            start_date,
            date.today()
        )
        
        ecritures = await self._get_ecritures_parcelle(
            parcelle_id,
            start_date,
            date.today()
        )
        
        return {
            "transactions": transactions,
            "ecritures": ecritures,
            "monthly_stats": self._calculate_monthly_stats(
                transactions,
                ecritures
            )
        }

    def _calculate_monthly_stats(
        self,
        transactions: List[Transaction],
        ecritures: List[EcritureComptable]
    ) -> List[Dict[str, Any]]:
        """Calcule les statistiques mensuelles"""
        stats = []
        
        # Groupement par mois
        months = set()
        for t in transactions:
            months.add(t.date_transaction.strftime("%Y-%m"))
        for e in ecritures:
            months.add(e.date_ecriture.strftime("%Y-%m"))
            
        # Calcul stats par mois
        for month in sorted(months):
            month_transactions = [
                t for t in transactions 
                if t.date_transaction.strftime("%Y-%m") == month
            ]
            month_ecritures = [
                e for e in ecritures
                if e.date_ecriture.strftime("%Y-%m") == month
            ]
            
            stats.append({
                "month": month,
                "revenue": sum(t.montant for t in month_transactions if t.type_transaction == "RECETTE"),
                "costs": sum(t.montant for t in month_transactions if t.type_transaction == "DEPENSE"),
                "debit": sum(e.debit or 0 for e in month_ecritures),
                "credit": sum(e.credit or 0 for e in month_ecritures)
            })
            
        return stats

    async def _predict_month_performance(
        self,
        parcelle_id: str,
        target_date: date,
        features: np.ndarray
    ) -> Dict[str, Any]:
        """Prédit la performance pour un mois"""
        # TODO: Implémenter modèle ML
        # Pour l'instant, utilise une moyenne pondérée
        weights = np.array([0.1] * len(features))
        base_prediction = float(np.sum(features * weights))
        
        # Ajustement météo
        weather_impact = await self.weather_service.get_forecast_impact(target_date)
        adjusted_prediction = base_prediction * (1 + weather_impact["score"])
        
        return {
            "revenue": adjusted_prediction * 1.1,
            "costs": adjusted_prediction * 0.8,
            "confidence": 0.85,
            "weather_impact": weather_impact["score"]
        }

    async def _optimize_with_ml(
        self,
        current_costs: Dict[str, Any],
        weather_impact: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimise les coûts avec ML"""
        # TODO: Implémenter algorithme optimisation
        # Pour l'instant, utilise des règles simples
        optimized = {}
        savings = {}
        
        for category, amount in current_costs.items():
            if amount > 1000:  # Seuil arbitraire
                potential_saving = amount * 0.1  # 10% d'économie possible
                optimized[category] = amount - potential_saving
                savings[category] = potential_saving
                
        return {
            "costs": optimized,
            "savings": savings,
            "plan": [
                {
                    "category": cat,
                    "current": current_costs[cat],
                    "target": opt_amount,
                    "actions": ["Optimiser achats", "Négocier tarifs"]
                }
                for cat, opt_amount in optimized.items()
            ],
            "risks": [
                {
                    "category": cat,
                    "risk_level": "LOW",
                    "description": "Impact minimal sur qualité"
                }
                for cat in optimized.keys()
            ]
        }
