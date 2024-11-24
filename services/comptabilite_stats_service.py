"""
Service de statistiques comptables avec ML
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from models.comptabilite import (
    CompteComptable, 
    EcritureComptable,
    TypeCompte,
    StatutEcriture
)
from sqlalchemy import func, and_
from decimal import Decimal

from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.finance_comptabilite.analyse import AnalyseFinanceCompta

class ComptabiliteStatsService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db)
        self.cache = CacheService()
        self.analyse = AnalyseFinanceCompta(db)

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières avec ML"""
        # Stats de base
        basic_stats = await self._get_basic_stats()
        
        # Prédictions ML
        predictions = await self._get_ml_predictions()
        
        # Fusion des résultats
        return {
            **basic_stats,
            "predictions": predictions,
            "recommendations": await self._generate_recommendations(
                basic_stats,
                predictions
            )
        }

    async def get_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Analyse détaillée du budget avec ML"""
        # Analyse de base
        basic_analysis = await self._get_basic_budget_analysis(periode)
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(
            target_date=datetime.strptime(periode, "%Y-%m").date()
        )
        
        # Performance ML
        performance = await self.analyse.predict_performance(months_ahead=3)
        
        return {
            **basic_analysis,
            "optimization": optimization,
            "performance": performance,
            "recommendations": await self._generate_budget_recommendations(
                basic_analysis,
                optimization,
                performance
            )
        }

    async def get_cashflow(self, days: int = 30) -> List[Dict[str, Any]]:
        """Récupère les données de trésorerie avec ML"""
        # Données de base
        basic_cashflow = await self._get_basic_cashflow(days)
        
        # Analyse ML
        end_date = datetime.now(datetime.timezone.utc).date()
        start_date = end_date - timedelta(days=days)
        
        ml_analysis = await self.analyse.get_analyse_parcelle(
            parcelle_id=None,  # Analyse globale
            date_debut=start_date,
            date_fin=end_date,
            include_predictions=True
        )
        
        # Enrichissement des données
        for entry in basic_cashflow:
            date_entry = datetime.strptime(entry["date"], "%Y-%m-%d").date()
            
            # Ajout prédictions ML
            entry["ml_predictions"] = {
                "revenue": self._get_prediction_for_date(
                    ml_analysis["ml_analysis"]["predictions"],
                    date_entry,
                    "revenue"
                ),
                "costs": self._get_prediction_for_date(
                    ml_analysis["ml_analysis"]["predictions"],
                    date_entry,
                    "costs"
                )
            }
            
            # Ajout risques ML
            entry["ml_risks"] = [
                risk for risk in ml_analysis["ml_analysis"]["risks"]
                if self._risk_applies_to_date(risk, date_entry)
            ]
            
        return basic_cashflow

    async def _get_basic_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques de base"""
        now = datetime.now(datetime.timezone.utc)
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        # Chiffre d'affaires du mois
        revenue = self.db.query(
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.PRODUIT
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == current_month
        ).scalar() or 0

        # Chiffre d'affaires du mois précédent
        previous_revenue = self.db.query(
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.PRODUIT
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul des charges
        expenses = self.db.query(
            func.sum(EcritureComptable.debit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.CHARGE
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == current_month
        ).scalar() or 0

        previous_expenses = self.db.query(
            func.sum(EcritureComptable.debit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.CHARGE
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul de la trésorerie
        cashflow = self.db.query(
            func.sum(CompteComptable.solde_debit - CompteComptable.solde_credit)
        ).filter(
            CompteComptable.type_compte == TypeCompte.ACTIF,
            CompteComptable.actif == True
        ).scalar() or 0

        previous_cashflow = cashflow - (revenue - expenses)

        return {
            "revenue": float(revenue),
            "revenueVariation": self._calculate_variation(revenue, previous_revenue),
            "expenses": float(expenses),
            "expensesVariation": self._calculate_variation(expenses, previous_expenses),
            "profit": float(revenue - expenses),
            "profitVariation": self._calculate_variation(
                revenue - expenses,
                previous_revenue - previous_expenses
            ),
            "cashflow": float(cashflow),
            "cashflowVariation": self._calculate_variation(cashflow, previous_cashflow)
        }

    async def _get_ml_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML"""
        # Prédictions performance
        performance = await self.analyse.predict_performance(months_ahead=3)
        
        # Calcul tendances
        trends = {
            "revenue": self._calculate_trend(
                [p["revenue"] for p in performance["predictions"]]
            ),
            "costs": self._calculate_trend(
                [p["costs"] for p in performance["predictions"]]
            ),
            "margin": self._calculate_trend(
                [p["margin"] for p in performance["predictions"]]
            )
        }
        
        return {
            "next_3_months": performance["predictions"],
            "trends": trends,
            "risk_factors": performance["risk_factors"]
        }

    async def _get_basic_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Analyse budgétaire de base"""
        # Récupération des données budgétaires
        charges = await self._get_charges_by_categorie(periode)
        produits = await self._get_produits_by_categorie(periode)
        
        # Impact météo
        weather_impact = await self._analyze_weather_impact(periode)
        
        # Calcul des totaux
        total_prevu = sum(cat["prevu"] for cat in charges.values()) + sum(cat["prevu"] for cat in produits.values())
        total_realise = sum(cat["realise"] for cat in charges.values()) + sum(cat["realise"] for cat in produits.values())
        
        return {
            "total_prevu": float(total_prevu),
            "total_realise": float(total_realise),
            "categories": {**charges, **produits},
            "weather_impact": weather_impact
        }

    async def _get_basic_cashflow(self, days: int) -> List[Dict[str, Any]]:
        """Récupère les données de trésorerie de base"""
        end_date = datetime.now(datetime.timezone.utc).date()
        start_date = end_date - timedelta(days=days)
        
        # Récupération des écritures
        query = self.db.query(
            func.date_trunc('day', EcritureComptable.date_ecriture).label('date'),
            func.sum(EcritureComptable.debit).label('sorties'),
            func.sum(EcritureComptable.credit).label('entrees')
        ).filter(
            EcritureComptable.date_ecriture.between(start_date, end_date),
            EcritureComptable.statut == StatutEcriture.VALIDEE
        ).group_by(
            func.date_trunc('day', EcritureComptable.date_ecriture)
        ).order_by(
            func.date_trunc('day', EcritureComptable.date_ecriture)
        )

        results = []
        solde_cumule = self._get_solde_initial(start_date)
        
        # Génération des données jour par jour
        current_date = start_date
        while current_date <= end_date:
            daily_data = query.filter(
                func.date_trunc('day', EcritureComptable.date_ecriture) == current_date
            ).first()

            entrees = float(daily_data.entrees if daily_data else 0)
            sorties = float(daily_data.sorties if daily_data else 0)
            solde_cumule += entrees - sorties

            # Récupération de l'impact météo
            weather_data = await self.weather_service.get_daily_impact(current_date)
            
            results.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "entrees": entrees,
                "sorties": sorties,
                "solde": float(solde_cumule),
                "impact_meteo": weather_data["impact"]
            })
            
            current_date += timedelta(days=1)

        return results

    def _calculate_variation(self, current: float, previous: float) -> Dict[str, Any]:
        """Calcule la variation entre deux valeurs"""
        if previous == 0:
            return {"value": 0, "type": "increase"}
        
        variation = ((current - previous) / abs(previous)) * 100
        return {
            "value": abs(round(variation, 1)),
            "type": "increase" if variation >= 0 else "decrease"
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calcule la tendance d'une série de valeurs"""
        if len(values) < 2:
            return "stable"
            
        trend = (values[-1] - values[0]) / values[0] if values[0] != 0 else 0
        
        if trend > 0.05:
            return "increasing"
        elif trend < -0.05:
            return "decreasing"
        else:
            return "stable"

    async def _generate_recommendations(
        self,
        stats: Dict[str, Any],
        predictions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur les stats et prédictions"""
        recommendations = []
        
        # Recommandations basées sur les stats actuelles
        if stats["profitVariation"]["type"] == "decrease":
            recommendations.append({
                "type": "PROFIT",
                "priority": "HIGH",
                "description": "Baisse de la rentabilité",
                "actions": [
                    "Analyser postes de coûts",
                    "Optimiser pricing",
                    "Revoir processus"
                ]
            })
            
        # Recommandations basées sur les prédictions
        for risk in predictions["risk_factors"]:
            recommendations.append({
                "type": "RISK",
                "priority": "MEDIUM",
                "description": f"Risque: {risk['factor']}",
                "actions": risk["mitigation"]
            })
            
        return recommendations

    async def _generate_budget_recommendations(
        self,
        analysis: Dict[str, Any],
        optimization: Dict[str, Any],
        performance: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations budgétaires"""
        recommendations = []
        
        # Recommandations d'optimisation
        if optimization["potential_savings"]:
            recommendations.append({
                "type": "OPTIMIZATION",
                "priority": "HIGH",
                "description": "Potentiel d'optimisation identifié",
                "actions": optimization["implementation_plan"],
                "expected_savings": optimization["potential_savings"]
            })
            
        # Recommandations de performance
        if performance["predictions"][0]["margin"] < 0:
            recommendations.append({
                "type": "PERFORMANCE",
                "priority": "HIGH",
                "description": "Marge négative prévue",
                "actions": [
                    "Revoir structure coûts",
                    "Optimiser revenus",
                    "Ajuster pricing"
                ]
            })
            
        return recommendations

    def _get_prediction_for_date(
        self,
        predictions: Dict[str, Any],
        target_date: date,
        metric: str
    ) -> float:
        """Récupère la prédiction pour une date donnée"""
        # TODO: Implémenter interpolation
        return predictions.get(metric, 0)

    def _risk_applies_to_date(
        self,
        risk: Dict[str, Any],
        target_date: date
    ) -> bool:
        """Vérifie si un risque s'applique à une date"""
        # TODO: Implémenter logique temporelle
        return True

    async def _get_charges_by_categorie(self, periode: str) -> Dict[str, Dict[str, float]]:
        """Récupère les charges par catégorie"""
        return await self._get_montants_by_categorie(TypeCompte.CHARGE, periode)

    async def _get_produits_by_categorie(self, periode: str) -> Dict[str, Dict[str, float]]:
        """Récupère les produits par catégorie"""
        return await self._get_montants_by_categorie(TypeCompte.PRODUIT, periode)

    async def _get_montants_by_categorie(
        self,
        type_compte: TypeCompte,
        periode: str
    ) -> Dict[str, Dict[str, float]]:
        """Récupère les montants par catégorie pour un type de compte"""
        query = self.db.query(
            CompteComptable.numero,
            CompteComptable.libelle,
            func.sum(EcritureComptable.debit).label('debit'),
            func.sum(EcritureComptable.credit).label('credit')
        ).join(
            EcritureComptable,
            CompteComptable.id == EcritureComptable.compte_id
        ).filter(
            CompteComptable.type_compte == type_compte,
            EcritureComptable.periode == periode
        ).group_by(
            CompteComptable.numero,
            CompteComptable.libelle
        )

        results = {}
        for row in query.all():
            montant = float(row.credit - row.debit if type_compte == TypeCompte.PRODUIT else row.debit - row.credit)
            results[row.numero] = {
                "libelle": row.libelle,
                "prevu": montant * 1.1,  # TODO: Implémenter la logique de budget prévisionnel
                "realise": montant
            }

        return results

    def _get_solde_initial(self, date: date) -> Decimal:
        """Calcule le solde initial à une date donnée"""
        return self.db.query(
            func.sum(CompteComptable.solde_debit - CompteComptable.solde_credit)
        ).filter(
            CompteComptable.type_compte == TypeCompte.ACTIF,
            CompteComptable.actif == True
        ).scalar() or Decimal('0')

    async def _analyze_weather_impact(self, periode: str) -> Dict[str, Any]:
        """Analyse l'impact de la météo sur les finances"""
        weather_data = await self.weather_service.get_monthly_stats(periode)
        
        impact = {
            "score": 0,
            "factors": [],
            "projections": {}
        }

        if weather_data.get("precipitation", 0) > 200:
            impact["score"] += 30
            impact["factors"].append("Fortes précipitations")
            impact["projections"]["TRANSPORT"] = "Augmentation probable des coûts"

        if weather_data.get("temperature_avg", 25) > 30:
            impact["score"] += 20
            impact["factors"].append("Températures élevées")
            impact["projections"]["MAINTENANCE"] = "Coûts supplémentaires possibles"

        return impact
