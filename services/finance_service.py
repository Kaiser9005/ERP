"""
Service de gestion financière avec ML
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from models.finance import Transaction, Compte, Budget, CategorieTransaction
from schemas.finance import TransactionCreate, BudgetCreate, BudgetUpdate
from sqlalchemy import func, and_
from services.weather_service import WeatherService
from services.cache_service import CacheService
from services.finance_comptabilite.analyse import AnalyseFinanceCompta

class FinanceService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.cache = CacheService()
        self.analyse = AnalyseFinanceCompta(db)

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières avec ML"""
        # Vérification cache
        cache_key = f"finance_stats_{datetime.utcnow().strftime('%Y-%m-%d')}"
        cached_stats = await self.cache.get(cache_key)
        if cached_stats:
            return cached_stats

        # Stats de base
        basic_stats = await self._get_basic_stats()
        
        # Prédictions ML
        ml_predictions = await self.analyse.predict_performance(months_ahead=3)
        
        # Optimisations ML
        optimization = await self.analyse.optimize_costs(
            target_date=datetime.utcnow().date()
        )
        
        # Fusion des résultats
        stats = {
            **basic_stats,
            "predictions": ml_predictions,
            "optimization": optimization,
            "recommendations": await self._generate_recommendations(
                basic_stats,
                ml_predictions,
                optimization
            )
        }
        
        # Mise en cache
        await self.cache.set(cache_key, stats, expire=3600)
        
        return stats

    async def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        """Crée une nouvelle transaction et met à jour les soldes"""
        db_transaction = Transaction(**transaction.dict())
        self.db.add(db_transaction)

        # Mise à jour des soldes des comptes
        if transaction.type_transaction == "RECETTE":
            await self._handle_recette(transaction)
        elif transaction.type_transaction == "DEPENSE":
            await self._handle_depense(transaction)
        elif transaction.type_transaction == "VIREMENT":
            await self._handle_virement(transaction)

        # Mise à jour du budget réalisé
        await self._update_budget_realise(transaction)

        # Invalidation du cache
        await self.cache.delete(f"finance_stats_{datetime.utcnow().strftime('%Y-%m-%d')}")
        await self.cache.delete(f"budget_analysis_{transaction.date_transaction.strftime('%Y-%m')}")

        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    async def create_budget(self, budget: BudgetCreate) -> Budget:
        """Crée un nouveau budget avec ML"""
        # Analyse ML pour optimisation
        optimization = await self.analyse.optimize_costs(
            target_date=datetime.strptime(budget.periode, "%Y-%m").date()
        )
        
        # Ajustement du budget selon ML
        if optimization["potential_savings"]:
            budget.montant_prevu = float(budget.montant_prevu) - float(optimization["potential_savings"])
        
        db_budget = Budget(**budget.dict())
        self.db.add(db_budget)
        
        # Invalidation cache
        await self.cache.delete(f"budget_analysis_{budget.periode}")
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    async def get_budgets(self, periode: Optional[str] = None) -> List[Budget]:
        """Récupère les budgets avec ML"""
        # Vérification cache
        cache_key = f"budgets_{periode or 'all'}"
        cached_budgets = await self.cache.get(cache_key)
        if cached_budgets:
            return cached_budgets

        # Requête base
        query = self.db.query(Budget)
        if periode:
            query = query.filter(Budget.periode == periode)
            
        budgets = query.all()
        
        # Enrichissement ML
        if periode:
            ml_analysis = await self.analyse.get_analyse_parcelle(
                parcelle_id=None,
                date_debut=datetime.strptime(periode, "%Y-%m").date(),
                date_fin=datetime.strptime(periode, "%Y-%m").date() + timedelta(days=30)
            )
            
            for budget in budgets:
                budget.ml_predictions = ml_analysis["ml_analysis"]["predictions"]
                budget.ml_recommendations = ml_analysis["ml_analysis"]["recommendations"]
        
        # Mise en cache
        await self.cache.set(cache_key, budgets, expire=3600)
        
        return budgets

    async def update_budget(self, budget_id: str, budget_update: BudgetUpdate) -> Budget:
        """Met à jour un budget avec ML"""
        db_budget = self.db.query(Budget).filter(Budget.id == budget_id).first()
        if not db_budget:
            raise ValueError("Budget non trouvé")
        
        # Analyse ML pour optimisation
        if "montant_prevu" in budget_update.dict(exclude_unset=True):
            optimization = await self.analyse.optimize_costs(
                target_date=datetime.strptime(db_budget.periode, "%Y-%m").date()
            )
            if optimization["potential_savings"]:
                budget_update.montant_prevu = float(budget_update.montant_prevu) - float(optimization["potential_savings"])
        
        for field, value in budget_update.dict(exclude_unset=True).items():
            setattr(db_budget, field, value)
        
        # Invalidation cache
        await self.cache.delete(f"budget_analysis_{db_budget.periode}")
        await self.cache.delete(f"budgets_{db_budget.periode}")
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    async def get_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Analyse détaillée du budget avec ML"""
        # Vérification cache
        cache_key = f"budget_analysis_{periode}"
        cached_analysis = await self.cache.get(cache_key)
        if cached_analysis:
            return cached_analysis

        # Analyse de base
        budgets = await self.get_budgets(periode)
        
        analysis = {
            "total_prevu": 0,
            "total_realise": 0,
            "categories": {},
            "weather_impact": await self._analyze_weather_impact(periode)
        }

        for budget in budgets:
            cat = budget.categorie.value
            analysis["categories"][cat] = {
                "prevu": float(budget.montant_prevu),
                "realise": float(budget.montant_realise),
                "ecart": float(budget.montant_realise - budget.montant_prevu),
                "ecart_percentage": round((budget.montant_realise - budget.montant_prevu) / budget.montant_prevu * 100, 2) if budget.montant_prevu != 0 else 0
            }
            analysis["total_prevu"] += float(budget.montant_prevu)
            analysis["total_realise"] += float(budget.montant_realise)

        # Enrichissement ML
        target_date = datetime.strptime(periode, "%Y-%m").date()
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(target_date=target_date)
        
        # Performance ML
        performance = await self.analyse.predict_performance(months_ahead=3)
        
        # Fusion résultats
        analysis.update({
            "optimization": optimization,
            "performance": performance,
            "recommendations": await self._generate_budget_recommendations(
                analysis,
                optimization,
                performance
            )
        })
        
        # Mise en cache
        await self.cache.set(cache_key, analysis, expire=3600)
        
        return analysis

    async def get_financial_projections(self, months_ahead: int = 3) -> Dict[str, Any]:
        """Génère des projections financières avec ML"""
        # Vérification cache
        cache_key = f"projections_{months_ahead}_{datetime.utcnow().strftime('%Y-%m-%d')}"
        cached_projections = await self.cache.get(cache_key)
        if cached_projections:
            return cached_projections

        now = datetime.utcnow()
        projections = {
            "revenue": [],
            "expenses": [],
            "weather_factors": [],
            "ml_predictions": []
        }

        # Analyse ML
        ml_performance = await self.analyse.predict_performance(months_ahead=months_ahead)
        
        for i in range(months_ahead):
            target_date = now + timedelta(days=30 * i)
            period = target_date.strftime("%Y-%m")
            
            # Analyse météo
            weather_impact = await self._analyze_weather_impact(period)
            
            # Calcul projections
            base_revenue = await self._calculate_base_projection("RECETTE", period)
            base_expenses = await self._calculate_base_projection("DEPENSE", period)
            
            # Ajustement météo
            weather_adjustment = weather_impact["score"] / 100
            adjusted_revenue = base_revenue * (1 - weather_adjustment * 0.1)
            adjusted_expenses = base_expenses * (1 + weather_adjustment * 0.15)
            
            # Fusion avec ML
            ml_prediction = ml_performance["predictions"][i]
            
            projections["revenue"].append({
                "period": period,
                "amount": round(adjusted_revenue, 2),
                "weather_impact": weather_impact["score"],
                "ml_prediction": ml_prediction["revenue"]
            })
            
            projections["expenses"].append({
                "period": period,
                "amount": round(adjusted_expenses, 2),
                "weather_impact": weather_impact["score"],
                "ml_prediction": ml_prediction["costs"]
            })
            
            projections["weather_factors"].extend(weather_impact["factors"])
            projections["ml_predictions"].append(ml_prediction)
        
        # Mise en cache
        await self.cache.set(cache_key, projections, expire=3600)
        
        return projections

    async def _get_basic_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques de base"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        # Chiffre d'affaires
        revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        previous_revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Charges
        expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        previous_expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calculs
        profit = revenue - expenses
        previous_profit = previous_revenue - previous_expenses

        # Trésorerie
        cashflow = self.db.query(
            func.sum(Compte.solde)
        ).filter(
            Compte.actif == True
        ).scalar() or 0

        previous_cashflow = cashflow - (revenue - expenses)

        return {
            "revenue": float(revenue),
            "revenueVariation": self._calculate_variation(revenue, previous_revenue),
            "expenses": float(expenses),
            "expensesVariation": self._calculate_variation(expenses, previous_expenses),
            "profit": float(profit),
            "profitVariation": self._calculate_variation(profit, previous_profit),
            "cashflow": float(cashflow),
            "cashflowVariation": self._calculate_variation(cashflow, previous_cashflow)
        }

    def _calculate_variation(
        self,
        current_value: float,
        previous_value: float
    ) -> Dict[str, Any]:
        """Calcule la variation entre deux valeurs"""
        if previous_value == 0:
            return {
                "value": 0,
                "type": "increase"
            }

        variation = ((current_value - previous_value) / previous_value) * 100
        return {
            "value": abs(round(variation, 1)),
            "type": "increase" if variation >= 0 else "decrease"
        }

    async def _handle_recette(self, transaction: TransactionCreate):
        """Gère une transaction de type recette"""
        compte = self.db.query(Compte).filter(
            Compte.id == transaction.compte_destination_id
        ).first()
        if not compte:
            raise ValueError("Compte de destination non trouvé")
        compte.solde += transaction.montant

    async def _handle_depense(self, transaction: TransactionCreate):
        """Gère une transaction de type dépense"""
        compte = self.db.query(Compte).filter(
            Compte.id == transaction.compte_source_id
        ).first()
        if not compte:
            raise ValueError("Compte source non trouvé")
        if compte.solde < transaction.montant:
            raise ValueError("Solde insuffisant")
        compte.solde -= transaction.montant

    async def _handle_virement(self, transaction: TransactionCreate):
        """Gère un virement entre comptes"""
        await self._handle_depense(transaction)
        await self._handle_recette(transaction)

    async def _update_budget_realise(self, transaction: TransactionCreate):
        """Met à jour le montant réalisé du budget"""
        periode = transaction.date_transaction.strftime("%Y-%m")
        
        budget = self.db.query(Budget).filter(
            and_(
                Budget.periode == periode,
                Budget.categorie == transaction.categorie
            )
        ).first()

        if budget:
            if transaction.type_transaction == "DEPENSE":
                budget.montant_realise += transaction.montant
            elif transaction.type_transaction == "RECETTE":
                budget.montant_realise += transaction.montant

    async def _analyze_weather_impact(self, periode: str) -> Dict[str, Any]:
        """Analyse l'impact de la météo avec ML"""
        # Vérification cache
        cache_key = f"weather_impact_{periode}"
        cached_impact = await self.cache.get(cache_key)
        if cached_impact:
            return cached_impact

        # Données météo
        weather_data = await self.weather_service.get_monthly_stats(periode)
        
        # Analyse ML
        target_date = datetime.strptime(periode, "%Y-%m").date()
        ml_analysis = await self.analyse.get_analyse_parcelle(
            parcelle_id=None,
            date_debut=target_date,
            date_fin=target_date + timedelta(days=30)
        )
        
        # Impact de base
        impact = {
            "score": 0,
            "factors": [],
            "projections": {}
        }

        # Analyse précipitations
        if weather_data.get("precipitation", 0) > 200:
            impact["score"] += 30
            impact["factors"].append("Fortes précipitations")
            impact["projections"]["TRANSPORT"] = "Augmentation probable des coûts"

        # Analyse températures
        if weather_data.get("temperature_avg", 25) > 30:
            impact["score"] += 20
            impact["factors"].append("Températures élevées")
            impact["projections"]["MAINTENANCE"] = "Coûts supplémentaires possibles"

        # Enrichissement ML
        impact.update({
            "ml_analysis": ml_analysis["ml_analysis"],
            "recommendations": ml_analysis["recommendations"]
        })
        
        # Mise en cache
        await self.cache.set(cache_key, impact, expire=3600)
        
        return impact

    async def _calculate_base_projection(
        self,
        type_transaction: str,
        target_period: str
    ) -> float:
        """Calcule la projection de base"""
        three_months_ago = (
            datetime.strptime(target_period, "%Y-%m") - timedelta(days=90)
        ).strftime("%Y-%m")
        
        avg_amount = self.db.query(
            func.avg(Transaction.montant)
        ).filter(
            Transaction.type_transaction == type_transaction,
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') >= three_months_ago
        ).scalar() or 0
        
        return float(avg_amount)

    async def _generate_recommendations(
        self,
        stats: Dict[str, Any],
        predictions: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur ML"""
        recommendations = []
        
        # Recommandations basées sur les stats
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
            
        # Recommandations ML
        if predictions["risk_factors"]:
            for risk in predictions["risk_factors"]:
                recommendations.append({
                    "type": "RISK",
                    "priority": risk["severity"],
                    "description": f"Risque: {risk['factor']}",
                    "actions": risk["mitigation"]
                })
                
        # Recommandations optimisation
        if optimization["potential_savings"]:
            recommendations.append({
                "type": "OPTIMIZATION",
                "priority": "HIGH",
                "description": "Potentiel d'optimisation identifié",
                "actions": optimization["implementation_plan"],
                "expected_savings": optimization["potential_savings"]
            })
            
        return recommendations

    async def _generate_budget_recommendations(
        self,
        analysis: Dict[str, Any],
        optimization: Dict[str, Any],
        performance: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations budgétaires ML"""
        recommendations = []
        
        # Recommandations écarts
        for cat, data in analysis["categories"].items():
            if data["ecart_percentage"] < -10:
                recommendations.append({
                    "type": "BUDGET_GAP",
                    "priority": "HIGH",
                    "description": f"Dépassement important du budget {cat}",
                    "value": abs(data["ecart_percentage"]),
                    "actions": [
                        "Analyser causes dépassement",
                        "Revoir allocation budget",
                        "Optimiser coûts"
                    ]
                })
            elif data["ecart_percentage"] > 10:
                recommendations.append({
                    "type": "BUDGET_GAP",
                    "priority": "MEDIUM",
                    "description": f"Sous-utilisation du budget {cat}",
                    "value": data["ecart_percentage"],
                    "actions": [
                        "Réallouer ressources",
                        "Ajuster prévisions",
                        "Identifier opportunités"
                    ]
                })
                
        # Recommandations optimisation
        if optimization["potential_savings"]:
            recommendations.append({
                "type": "OPTIMIZATION",
                "priority": "HIGH",
                "description": "Potentiel d'optimisation identifié",
                "actions": optimization["implementation_plan"],
                "expected_savings": optimization["potential_savings"]
            })
            
        # Recommandations performance
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
