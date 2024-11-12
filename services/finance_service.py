from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from models.finance import Transaction, Compte, Budget, CategorieTransaction
from schemas.finance import TransactionCreate, BudgetCreate, BudgetUpdate
from sqlalchemy import func, and_
from services.weather_service import WeatherService

class FinanceService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        # Chiffre d'affaires du mois
        revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        # Chiffre d'affaires du mois précédent
        previous_revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul des variations
        revenue_variation = self._calculate_variation(revenue, previous_revenue)

        # Calcul du bénéfice
        expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        profit = revenue - expenses
        previous_expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        previous_profit = previous_revenue - previous_expenses
        profit_variation = self._calculate_variation(profit, previous_profit)

        # Calcul de la trésorerie
        cashflow = self.db.query(
            func.sum(Compte.solde)
        ).filter(
            Compte.actif == True
        ).scalar() or 0

        return {
            "revenue": revenue,
            "revenueVariation": revenue_variation,
            "profit": profit,
            "profitVariation": profit_variation,
            "cashflow": cashflow,
            "cashflowVariation": {
                "value": 0,  # À implémenter
                "type": "increase"
            },
            "expenses": expenses,
            "expensesVariation": self._calculate_variation(expenses, previous_expenses)
        }

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

        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

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

    # Nouvelles méthodes pour la gestion budgétaire

    async def create_budget(self, budget: BudgetCreate) -> Budget:
        """Crée un nouveau budget pour une période et une catégorie"""
        db_budget = Budget(**budget.dict())
        self.db.add(db_budget)
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    async def get_budgets(self, periode: Optional[str] = None) -> List[Budget]:
        """Récupère les budgets pour une période donnée"""
        query = self.db.query(Budget)
        if periode:
            query = query.filter(Budget.periode == periode)
        return query.all()

    async def update_budget(self, budget_id: str, budget_update: BudgetUpdate) -> Budget:
        """Met à jour un budget existant"""
        db_budget = self.db.query(Budget).filter(Budget.id == budget_id).first()
        if not db_budget:
            raise ValueError("Budget non trouvé")
        
        for field, value in budget_update.dict(exclude_unset=True).items():
            setattr(db_budget, field, value)
        
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    async def get_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Analyse détaillée du budget pour une période"""
        budgets = await self.get_budgets(periode)
        
        analysis = {
            "total_prevu": 0,
            "total_realise": 0,
            "categories": {},
            "weather_impact": await self._analyze_weather_impact(periode),
            "recommendations": []
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

        # Génération des recommandations
        for cat, data in analysis["categories"].items():
            if data["ecart_percentage"] < -10:
                analysis["recommendations"].append(
                    f"Dépassement important du budget {cat}: {abs(data['ecart_percentage'])}% d'écart"
                )
            elif data["ecart_percentage"] > 10:
                analysis["recommendations"].append(
                    f"Sous-utilisation du budget {cat}: {data['ecart_percentage']}% d'écart"
                )

        return analysis

    async def _analyze_weather_impact(self, periode: str) -> Dict[str, Any]:
        """Analyse l'impact de la météo sur les finances"""
        weather_data = await self.weather_service.get_monthly_stats(periode)
        
        # Analyse des corrélations météo-finances
        impact = {
            "score": 0,  # Score d'impact de 0 à 100
            "factors": [],
            "projections": {}
        }

        # Analyse des précipitations
        if weather_data.get("precipitation", 0) > 200:  # Seuil de forte pluie
            impact["score"] += 30
            impact["factors"].append("Fortes précipitations")
            impact["projections"]["TRANSPORT"] = "Augmentation probable des coûts de transport"

        # Analyse des températures
        if weather_data.get("temperature_avg", 25) > 30:  # Seuil de chaleur
            impact["score"] += 20
            impact["factors"].append("Températures élevées")
            impact["projections"]["MAINTENANCE"] = "Augmentation possible des coûts de maintenance"

        return impact

    async def _update_budget_realise(self, transaction: TransactionCreate):
        """Met à jour le montant réalisé du budget correspondant"""
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
                # Pour les recettes, on peut avoir un budget de revenus
                budget.montant_realise += transaction.montant

    async def get_financial_projections(self, months_ahead: int = 3) -> Dict[str, Any]:
        """Génère des projections financières basées sur l'historique et la météo"""
        now = datetime.utcnow()
        projections = {
            "revenue": [],
            "expenses": [],
            "weather_factors": []
        }

        for i in range(months_ahead):
            target_date = now + timedelta(days=30 * i)
            period = target_date.strftime("%Y-%m")
            
            # Analyse météo pour la période
            weather_impact = await self._analyze_weather_impact(period)
            
            # Calcul des projections
            base_revenue = await self._calculate_base_projection("RECETTE", period)
            base_expenses = await self._calculate_base_projection("DEPENSE", period)
            
            # Ajustement selon l'impact météo
            weather_adjustment = weather_impact["score"] / 100
            adjusted_revenue = base_revenue * (1 - weather_adjustment * 0.1)  # Max 10% impact
            adjusted_expenses = base_expenses * (1 + weather_adjustment * 0.15)  # Max 15% impact
            
            projections["revenue"].append({
                "period": period,
                "amount": round(adjusted_revenue, 2),
                "weather_impact": weather_impact["score"]
            })
            
            projections["expenses"].append({
                "period": period,
                "amount": round(adjusted_expenses, 2),
                "weather_impact": weather_impact["score"]
            })
            
            projections["weather_factors"].extend(weather_impact["factors"])

        return projections

    async def _calculate_base_projection(self, type_transaction: str, target_period: str) -> float:
        """Calcule la projection de base pour un type de transaction"""
        # Moyenne des 3 derniers mois
        three_months_ago = (datetime.strptime(target_period, "%Y-%m") - timedelta(days=90)).strftime("%Y-%m")
        
        avg_amount = self.db.query(
            func.avg(Transaction.montant)
        ).filter(
            Transaction.type_transaction == type_transaction,
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') >= three_months_ago
        ).scalar() or 0
        
        return float(avg_amount)
